"""End-to-end ingestion pipeline.

For each enabled source:
    fetch RSS → for each entry:
        upsert item (by url) → if new:
            embed → dedupe check → summarize → classify → persist

The pipeline is idempotent. Re-running it does not create duplicates;
unique constraints on items.url and primary keys on the child tables
make every step a safe upsert.
"""

from __future__ import annotations

from dataclasses import dataclass

from tenacity import retry, stop_after_attempt, wait_exponential_jitter

from workers.ai.classify import classify
from workers.ai.dedupe import find_duplicate
from workers.ai.embed import embed
from workers.ai.summarize import summarize
from workers.config import settings
from workers.db import supabase
from workers.ingest.rss import RawItem, poll
from workers.logging import get_logger

log = get_logger(__name__)


@dataclass
class PipelineStats:
    sources: int = 0
    fetched: int = 0
    new_items: int = 0
    deduped: int = 0
    summarized: int = 0
    errors: int = 0


def _run_for_source(source_row: dict, stats: PipelineStats) -> None:
    result = poll(
        source_id=source_row["id"],
        source_name=source_row["name"],
        url=source_row["url"],
        etag=source_row.get("etag"),
        last_modified=source_row.get("last_modified"),
    )
    stats.fetched += len(result.items)

    for raw in result.items:
        try:
            _process_item(raw, stats)
        except Exception as exc:
            stats.errors += 1
            log.error("pipeline.item_failed", url=raw.url, error=str(exc))

    sb = supabase()
    sb.table("sources").update(
        {
            "last_polled_at": "now()",
            "etag": result.new_etag,
            "last_modified": result.new_last_modified,
        }
    ).eq("id", source_row["id"]).execute()


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=1, max=8))
def _process_item(raw: RawItem, stats: PipelineStats) -> None:
    sb = supabase()

    existing = (
        sb.table("items").select("id").eq("url", raw.url).limit(1).execute()
    )
    if existing.data:
        return  # already ingested

    # Reserve the row first so concurrent runs don't double-process.
    inserted = (
        sb.table("items")
        .upsert(
            {
                "source_id": raw.source_id,
                "external_id": raw.external_id,
                "url": raw.url,
                "title": raw.title,
                "author": raw.author,
                "raw_content": raw.raw_content,
                "raw_html": raw.raw_html,
                "published_at": raw.published_at.isoformat(),
            },
            on_conflict="url",
            returning="representation",
        )
        .execute()
    )
    if not inserted.data:
        return
    item_id = inserted.data[0]["id"]
    stats.new_items += 1

    summary_input = f"{raw.title}\n\n{raw.raw_content or ''}"
    vector = embed(summary_input)

    dup = find_duplicate(vector)
    if dup:
        # Roll back: delete the placeholder row we just created.
        sb.table("items").delete().eq("id", item_id).execute()
        stats.deduped += 1
        stats.new_items -= 1
        return

    sb.table("item_embeddings").upsert(
        {
            "item_id": item_id,
            "model": settings.openai_embedding_model,
            "embedding": vector,
        }
    ).execute()

    summary = summarize(title=raw.title, source=raw.source_name, content=raw.raw_content or "")
    sb.table("item_summaries").upsert(
        {
            "item_id": item_id,
            "model": summary.model,
            "short": summary.short,
            "bullets": summary.bullets,
            "impact": summary.impact,
        }
    ).execute()
    stats.summarized += 1

    cats = classify(title=raw.title, content=raw.raw_content or "")
    if cats:
        sb.table("item_categories").upsert(
            [{"item_id": item_id, "category": c, "confidence": 0.9} for c in cats]
        ).execute()


def run_once() -> PipelineStats:
    sb = supabase()
    stats = PipelineStats()
    sources = sb.table("sources").select("*").eq("enabled", True).execute().data
    stats.sources = len(sources)
    log.info("pipeline.start", sources=stats.sources)

    for row in sources:
        try:
            _run_for_source(row, stats)
        except Exception as exc:
            stats.errors += 1
            log.error("pipeline.source_failed", source=row.get("name"), error=str(exc))

    log.info("pipeline.done", **stats.__dict__)
    return stats
