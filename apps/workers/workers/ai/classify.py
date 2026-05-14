"""Hybrid classifier: rule-based first, LLM fallback.

Categories mirror the `item_category` enum in 0001_init.sql.
"""

from __future__ import annotations

import json
import re

from workers.ai.llm import get_classify_provider
from workers.logging import get_logger

log = get_logger(__name__)

CATEGORIES = [
    "llms",
    "robotics",
    "humanoids",
    "multimodal",
    "agents",
    "infrastructure",
    "ai_chips",
    "open_source",
    "ai_video",
    "ai_audio",
    "healthcare_ai",
    "defense_ai",
    "regulation",
    "research",
    "funding",
    "product_launch",
    "other",
]

# Cheap keyword pre-filters — applied to lowercased "title + short content".
_RULES: list[tuple[str, list[str]]] = [
    ("humanoids", ["humanoid", "bipedal robot", "figure 02", "figure 01", "optimus", "1x neo"]),
    ("robotics", ["robot", "robotics", "manipulation", "quadruped", "drone"]),
    ("ai_chips", ["gpu", "tpu", "asic", "nvidia h", "nvidia b", "blackwell", "groq lpu", "trainium"]),
    ("agents", ["agent", "tool use", "computer use", "autonomous agent"]),
    ("multimodal", ["multimodal", "vision-language", "vlm", "image-to-text", "video-to-text"]),
    ("ai_video", ["video generation", "text-to-video", "sora", "veo", "runway"]),
    ("ai_audio", ["text-to-speech", "tts", "speech model", "audio generation"]),
    ("regulation", ["regulation", "executive order", "ai act", "policy", "compliance"]),
    ("funding", ["seed round", "series a", "series b", "series c", "raised $", "valuation"]),
    ("open_source", ["open source", "open-weight", "open weights", "apache 2.0", "mit license"]),
    ("research", ["arxiv", "paper", "preprint", "benchmark", "evaluation"]),
    ("llms", ["llm", "language model", "gpt-", "claude ", "gemini ", "llama ", "mistral "]),
]


def _rule_match(text: str) -> list[str]:
    text = text.lower()
    hits: list[str] = []
    for cat, terms in _RULES:
        if any(t in text for t in terms):
            hits.append(cat)
    return hits


SYSTEM = """Classify an AI/robotics news item into 1-3 categories from this fixed list:
llms, robotics, humanoids, multimodal, agents, infrastructure, ai_chips, open_source,
ai_video, ai_audio, healthcare_ai, defense_ai, regulation, research, funding,
product_launch, other.

Return strict JSON: {"categories": ["cat1", "cat2"]}. No prose. No code fences."""


_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def classify(*, title: str, content: str) -> list[str]:
    text = f"{title}\n{(content or '')[:1500]}"
    rule_hits = _rule_match(text)
    if rule_hits:
        return list(dict.fromkeys(rule_hits))[:3]

    provider = get_classify_provider()
    raw = provider.complete(
        system=SYSTEM,
        user=text,
        max_tokens=80,
        temperature=0.0,
    )
    match = _JSON_RE.search(raw)
    if not match:
        return ["other"]
    try:
        data = json.loads(match.group(0))
    except json.JSONDecodeError:
        return ["other"]
    cats = [c for c in (data.get("categories") or []) if c in CATEGORIES]
    return cats[:3] or ["other"]
