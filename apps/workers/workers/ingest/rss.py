"""RSS poller.

For each enabled source row, refetch using ETag / Last-Modified hints
when present. Returns a list of normalized "raw items" — the pipeline
is responsible for downstream processing.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any

import feedparser
from bs4 import BeautifulSoup

from workers.logging import get_logger

log = get_logger(__name__)


@dataclass
class RawItem:
    source_id: str
    source_name: str
    external_id: str | None
    url: str
    title: str
    author: str | None
    raw_html: str | None
    raw_content: str | None
    published_at: datetime


@dataclass
class PollResult:
    source_id: str
    items: list[RawItem]
    new_etag: str | None
    new_last_modified: str | None


def _strip_html(html: str | None) -> str | None:
    if not html:
        return None
    soup = BeautifulSoup(html, "lxml")
    text = soup.get_text(separator=" ", strip=True)
    return text or None


def _parse_published(entry: dict[str, Any]) -> datetime:
    for key in ("published_parsed", "updated_parsed", "created_parsed"):
        value = entry.get(key)
        if value:
            return datetime(*value[:6], tzinfo=timezone.utc)
    return datetime.now(tz=timezone.utc)


def _content_html(entry: dict[str, Any]) -> str | None:
    if "content" in entry and entry["content"]:
        return entry["content"][0].get("value")
    return entry.get("summary")


def poll(
    *,
    source_id: str,
    source_name: str,
    url: str,
    etag: str | None,
    last_modified: str | None,
) -> PollResult:
    log.info("rss.poll", source=source_name, url=url)

    parsed = feedparser.parse(
        url,
        etag=etag or None,
        modified=last_modified or None,
        request_headers={"User-Agent": "TownCrier/0.1 (+https://github.com/town-crier)"},
    )

    # 304 Not Modified → empty items, keep existing hints.
    if getattr(parsed, "status", None) == 304:
        log.info("rss.not_modified", source=source_name)
        return PollResult(source_id=source_id, items=[], new_etag=etag, new_last_modified=last_modified)

    items: list[RawItem] = []
    for entry in parsed.entries:
        link = entry.get("link")
        title = entry.get("title")
        if not link or not title:
            continue
        html = _content_html(entry)
        items.append(
            RawItem(
                source_id=source_id,
                source_name=source_name,
                external_id=entry.get("id") or entry.get("guid"),
                url=link,
                title=title.strip(),
                author=entry.get("author"),
                raw_html=html,
                raw_content=_strip_html(html),
                published_at=_parse_published(entry),
            )
        )

    log.info("rss.fetched", source=source_name, count=len(items))
    return PollResult(
        source_id=source_id,
        items=items,
        new_etag=getattr(parsed, "etag", None) or etag,
        new_last_modified=getattr(parsed, "modified", None) or last_modified,
    )
