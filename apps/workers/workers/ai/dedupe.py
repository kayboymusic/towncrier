"""Embedding-based near-duplicate detection.

Compares a candidate embedding against item embeddings from the last
`DEDUP_LOOKBACK_DAYS` days using cosine distance via pgvector's `<=>`
operator. A match is considered a duplicate when similarity exceeds
`DEDUP_SIMILARITY_THRESHOLD`.
"""

from __future__ import annotations

import psycopg

from workers.config import settings
from workers.logging import get_logger

log = get_logger(__name__)


def _vector_literal(v: list[float]) -> str:
    return "[" + ",".join(f"{x:.7f}" for x in v) + "]"


def find_duplicate(embedding: list[float]) -> str | None:
    """Return the existing item_id if a near-duplicate is found, else None."""
    if not settings.database_url:
        # Without a direct Postgres connection we can't run pgvector ops;
        # the upsert path will still de-dupe on `items.url` uniqueness.
        return None

    threshold = settings.dedup_similarity_threshold
    distance_cutoff = 1.0 - threshold

    with psycopg.connect(settings.database_url) as conn, conn.cursor() as cur:
        cur.execute(
            """
            select e.item_id, (e.embedding <=> %s::vector) as distance
              from item_embeddings e
              join items i on i.id = e.item_id
             where i.published_at > now() - (%s || ' days')::interval
             order by e.embedding <=> %s::vector
             limit 1
            """,
            (_vector_literal(embedding), str(settings.dedup_lookback_days), _vector_literal(embedding)),
        )
        row = cur.fetchone()
        if not row:
            return None
        item_id, distance = row
        if distance is not None and distance <= distance_cutoff:
            log.info("dedupe.match", item_id=str(item_id), distance=float(distance))
            return str(item_id)
        return None
