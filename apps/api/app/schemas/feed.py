from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel


class CompanyRef(BaseModel):
    slug: str
    name: str


class FeedItem(BaseModel):
    id: str
    url: str
    title: str
    author: str | None = None
    published_at: datetime
    fetched_at: datetime
    source_name: str | None = None
    source_homepage: str | None = None
    short_summary: str | None = None
    bullets: list[str] = []
    impact: str | None = None
    categories: list[str] = []
    companies: list[CompanyRef] = []


class FeedPage(BaseModel):
    items: list[FeedItem]
    next_cursor: str | None = None
