"""Seed list of ingestion sources.

Idempotently upserted into the `sources` table on first run.
Add or comment lines here to grow the surface area.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class SeedSource:
    name: str
    kind: str  # 'rss' | 'api' | 'scrape' | 'webhook'
    url: str
    homepage: str | None = None


SEED_SOURCES: list[SeedSource] = [
    SeedSource(
        name="Anthropic — News",
        kind="rss",
        url="https://www.anthropic.com/news/rss.xml",
        homepage="https://www.anthropic.com/news",
    ),
    SeedSource(
        name="Hugging Face — Blog",
        kind="rss",
        url="https://huggingface.co/blog/feed.xml",
        homepage="https://huggingface.co/blog",
    ),
    SeedSource(
        name="arXiv — cs.AI",
        kind="rss",
        url="http://export.arxiv.org/rss/cs.AI",
        homepage="https://arxiv.org/list/cs.AI/recent",
    ),
    SeedSource(
        name="IEEE Spectrum — Robotics",
        kind="rss",
        url="https://spectrum.ieee.org/feeds/topic/robotics.rss",
        homepage="https://spectrum.ieee.org/topic/robotics/",
    ),
]
