from __future__ import annotations

import base64
import json
from datetime import datetime

from app.core.config import settings
from app.db.supabase import supabase
from app.schemas.feed import CompanyRef, FeedItem, FeedPage


def _encode_cursor(published_at: str, item_id: str) -> str:
    raw = json.dumps({"p": published_at, "i": item_id})
    return base64.urlsafe_b64encode(raw.encode()).decode().rstrip("=")


def _decode_cursor(cursor: str) -> tuple[str, str]:
    padding = "=" * (-len(cursor) % 4)
    raw = base64.urlsafe_b64decode((cursor + padding).encode()).decode()
    data = json.loads(raw)
    return data["p"], data["i"]


def _row_to_item(row: dict) -> FeedItem:
    return FeedItem(
        id=row["id"],
        url=row["url"],
        title=row["title"],
        author=row.get("author"),
        published_at=row["published_at"],
        fetched_at=row["fetched_at"],
        source_name=row.get("source_name"),
        source_homepage=row.get("source_homepage"),
        short_summary=row.get("short_summary"),
        bullets=row.get("bullets") or [],
        impact=row.get("impact"),
        categories=row.get("categories") or [],
        companies=[CompanyRef(**c) for c in (row.get("companies") or [])],
    )


def get_feed(
    *,
    limit: int | None = None,
    cursor: str | None = None,
    category: str | None = None,
) -> FeedPage:
    sb = supabase()
    page_size = min(limit or settings.default_feed_limit, settings.max_feed_limit)

    query = sb.table("feed_view").select("*")

    if cursor:
        cursor_pub, cursor_id = _decode_cursor(cursor)
        # Keyset pagination on (published_at desc, id desc).
        # Postgrest supports `or` filters for compound keyset conditions.
        query = query.or_(
            f"published_at.lt.{cursor_pub},"
            f"and(published_at.eq.{cursor_pub},id.lt.{cursor_id})"
        )

    if category:
        query = query.contains("categories", [category])

    rows = (
        query.order("published_at", desc=True)
        .order("id", desc=True)
        .limit(page_size + 1)
        .execute()
        .data
        or []
    )

    has_more = len(rows) > page_size
    rows = rows[:page_size]

    items = [_row_to_item(r) for r in rows]
    next_cursor: str | None = None
    if has_more and items:
        last = items[-1]
        next_cursor = _encode_cursor(
            published_at=last.published_at.isoformat() if isinstance(last.published_at, datetime) else str(last.published_at),
            item_id=last.id,
        )

    return FeedPage(items=items, next_cursor=next_cursor)
