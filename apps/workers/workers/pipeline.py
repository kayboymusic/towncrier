"""End-to-end ingestion pipeline.

Per run cycle:
    1. For each enabled source, poll the RSS feed and upsert every entry
       into `items` (cheap, no AI calls).
    2. Walk every item that's missing a summary OR embedding and fill it in.
       This second pass catches both "new this cycle" and "stranded from a
       prior crash / rate limit / partial run".

Idempotency guarantees:
    - `items.url` unique → re-fetching the same RSS entry never duplicates.
    - Child tables (`item_summaries`, `item_embeddings`, `item_categories`)
      are upserted by `item_id`, so re-processing overwrites cleanly.
    - Dedupe runs only the first time we successfully embed an item. If the
      item is already in `items` and we're just back-filling missing parts,
      dedupe is skipped (we don't want to delete a row we're trying to fix).
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
    enriched: int = 0
    deduped: int = 0
    errors: int = 0


def _ingest_items_from_source(source_row: dict, stats: PipelineStats) -> None:
    """Phase 1: cheap. Poll RSS, upsert items. No AI calls."""
    sb = supabase()
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
            _upsert_item_row(raw, stats)
        except Exception as exc:
            stats.errors += 1
            log.error("pipeline.upsert_failed", url=raw.url, error=str(exc))

    sb.table("sources").update(
        {
            "last_polled_at": "now()",
            "etag": result.new_etag,
            "last_modified": result.new_last_modified,
        }
    ).eq("id", source_row["id"]).execute()


def _upsert_item_row(raw: RawItem, stats: PipelineStats) -> None:
    sb = supabase()
    existing = (
        sb.table("items").select("id").eq("url", raw.url).limit(1).execute().data
    )
    if existing:
        return  # row already present; enrichment pass will handle missing parts

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
    if inserted.data:
        stats.new_items += 1


@retry(stop=stop_after_attempt(3), wait=wait_exponential_jitter(initial=1, max=8))
def _enrich_one(item: dict, stats: PipelineStats) -> None:
    """Phase 2: fill in missing summary/embedding/categories for one item.

    `item` is the joined row from the SQL below: id, url, title, author,
    raw_content, source_name, has_summary, has_embedding, has_categories.
    """
    sb = supabase()
    item_id = item["id"]

    title = item["title"]
    content = item.get("raw_content") or ""
    source_name = item.get("source_name") or "unknown"

    if not item["has_embedding"]:
        vector = embed(f"{title}\n\n{content}")

        # Dedupe only runs the first time we embed (i.e. fresh items).
        # Skipping dedupe for items already in the DB avoids ever deleting
        # the row we're trying to back-fill.
        if not item["has_summary"]:
            dup = find_duplicate(vector)
            if dup and dup != item_id:
                sb.table("items").delete().eq("id", item_id).execute()
                stats.deduped += 1
                return

        sb.table("item_embeddings").upsert(
            {
                "item_id": item_id,
                "model": settings.openai_embedding_model,
                "embedding": vector,
            }
        ).execute()

    if not item["has_summary"]:
        s = summarize(title=title, source=source_name, content=content)
        sb.table("item_summaries").upsert(
            {
                "item_id": item_id,
                "model": s.model,
                "short": s.short,
                "bullets": s.bullets,
                "impact": s.impact,
            }
        ).execute()
        stats.enriched += 1

    if not item["has_categories"]:
        cats = classify(title=title, content=content)
        if cats:
            sb.table("item_categories").upsert(
                [{"item_id": item_id, "category": c, "confidence": 0.9} for c in cats]
            ).execute()


def _pending_items(limit: int = 500) -> list[dict]:
    """Items that are missing a summary OR embedding (the AI bits)."""
    import psycopg

    if not settings.database_url:
        # Without raw SQL access we can only do best-effort via PostgREST.
        sb = supabase()
        rows = (
            sb.table("items")
            .select("id,url,title,author,raw_content,sources(name)")
            .order("published_at", desc=True)
            .limit(limit)
            .execute()
            .data
            or []
        )
        out = []
        for r in rows:
            out.append(
                {
                    "id": r["id"],
                    "url": r["url"],
                    "title": r["title"],
                    "author": r.get("author"),
                    "raw_content": r.get("raw_content"),
                    "source_name": (r.get("sources") or {}).get("name"),
                    "has_summary": False,  # we don't know; let upsert handle it
                    "has_embedding": False,
                    "has_categories": False,
                }
            )
        return out

    with psycopg.connect(settings.database_url) as conn, conn.cursor() as cur:
        cur.execute(
            """
            select
              i.id,
              i.url,
              i.title,
              i.author,
              i.raw_content,
              s.name as source_name,
              (sm.item_id is not null) as has_summary,
              (em.item_id is not null) as has_embedding,
              exists(select 1 from item_categories ic where ic.item_id = i.id) as has_categories
            from items i
            left join sources s on s.id = i.source_id
            left join item_summaries sm on sm.item_id = i.id
            left join item_embeddings em on em.item_id = i.id
            where sm.item_id is null or em.item_id is null
            order by i.published_at desc
            limit %s
            """,
            (limit,),
        )
        cols = [d.name for d in cur.description]
        return [dict(zip(cols, row, strict=True)) for row in cur.fetchall()]


def _enrich_pending(stats: PipelineStats, batch_limit: int = 500) -> None:
    pending = _pending_items(limit=batch_limit)
    log.info("pipeline.enrich_pending", count=len(pending))
    for item in pending:
        try:
            _enrich_one(item, stats)
        except Exception as exc:
            stats.errors += 1
            log.error("pipeline.enrich_failed", item_id=item["id"], error=str(exc))


def run_once(*, enrich_limit: int = 500) -> PipelineStats:
    sb = supabase()
    stats = PipelineStats()
    sources = sb.table("sources").select("*").eq("enabled", True).execute().data
    stats.sources = len(sources)
    log.info("pipeline.start", sources=stats.sources)

    # Phase 1 — cheap, no AI calls. Get every new RSS entry into items.
    for row in sources:
        try:
            _ingest_items_from_source(row, stats)
        except Exception as exc:
            stats.errors += 1
            log.error("pipeline.source_failed", source=row.get("name"), error=str(exc))

    # Phase 2 — expensive, AI calls. Back-fill anything missing.
    _enrich_pending(stats, batch_limit=enrich_limit)

    log.info("pipeline.done", **stats.__dict__)
    return stats
