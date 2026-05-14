from __future__ import annotations

from fastapi import APIRouter, HTTPException, Query

from app.schemas.feed import FeedPage
from app.services import feed_service

router = APIRouter(prefix="/api/feed", tags=["feed"])


@router.get("", response_model=FeedPage)
def get_feed(
    limit: int = Query(default=25, ge=1, le=100),
    cursor: str | None = Query(default=None),
    category: str | None = Query(default=None),
) -> FeedPage:
    try:
        return feed_service.get_feed(limit=limit, cursor=cursor, category=category)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
