from __future__ import annotations

from fastapi import APIRouter, Query

router = APIRouter(prefix="/api/search", tags=["search"])


@router.get("")
def search(q: str = Query(...)) -> dict:
    # Stub — see PRD §6.6 / §18. Will combine FTS (tsvector) +
    # semantic search (pgvector) once wired.
    return {"query": q, "results": [], "stub": True}
