"""Idempotent seeders for sources + companies."""

from __future__ import annotations

from workers.db import supabase
from workers.ingest.sources import SEED_SOURCES
from workers.logging import get_logger

log = get_logger(__name__)


SEED_COMPANIES: list[dict] = [
    {"slug": "openai", "name": "OpenAI", "website": "https://openai.com", "twitter": "OpenAI"},
    {"slug": "anthropic", "name": "Anthropic", "website": "https://anthropic.com", "twitter": "AnthropicAI"},
    {"slug": "google-deepmind", "name": "Google DeepMind", "website": "https://deepmind.google", "twitter": "GoogleDeepMind"},
    {"slug": "meta-ai", "name": "Meta AI", "website": "https://ai.meta.com", "twitter": "MetaAI"},
    {"slug": "xai", "name": "xAI", "website": "https://x.ai", "twitter": "xai"},
    {"slug": "mistral", "name": "Mistral AI", "website": "https://mistral.ai", "twitter": "MistralAI"},
    {"slug": "hugging-face", "name": "Hugging Face", "website": "https://huggingface.co", "twitter": "huggingface", "github_org": "huggingface"},
    {"slug": "boston-dynamics", "name": "Boston Dynamics", "website": "https://bostondynamics.com", "twitter": "BostonDynamics"},
    {"slug": "figure", "name": "Figure", "website": "https://figure.ai", "twitter": "Figure_robot"},
    {"slug": "1x", "name": "1X Technologies", "website": "https://1x.tech", "twitter": "1x_tech"},
    {"slug": "tesla", "name": "Tesla", "website": "https://tesla.com", "twitter": "Tesla"},
    {"slug": "nvidia", "name": "NVIDIA", "website": "https://nvidia.com", "twitter": "nvidia"},
    {"slug": "cohere", "name": "Cohere", "website": "https://cohere.com", "twitter": "cohere"},
    {"slug": "stability-ai", "name": "Stability AI", "website": "https://stability.ai", "twitter": "StabilityAI"},
    {"slug": "runway", "name": "Runway", "website": "https://runwayml.com", "twitter": "runwayml"},
]


def seed_sources() -> int:
    sb = supabase()
    rows = [
        {"name": s.name, "kind": s.kind, "url": s.url, "homepage": s.homepage, "enabled": True}
        for s in SEED_SOURCES
    ]
    sb.table("sources").upsert(rows, on_conflict="url").execute()
    log.info("seed.sources", count=len(rows))
    return len(rows)


def seed_companies() -> int:
    sb = supabase()
    sb.table("companies").upsert(SEED_COMPANIES, on_conflict="slug").execute()
    log.info("seed.companies", count=len(SEED_COMPANIES))
    return len(SEED_COMPANIES)
