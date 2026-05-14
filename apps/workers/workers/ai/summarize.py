from __future__ import annotations

import json
import re
from dataclasses import dataclass

from workers.ai.llm import get_summary_provider
from workers.logging import get_logger

log = get_logger(__name__)

SYSTEM = """You are an AI/robotics news summarizer for "Town Crier".
Output strict JSON with this shape:
{
  "short": "1-2 sentence factual summary, <=240 chars, no marketing fluff",
  "bullets": ["3-5 concrete takeaways, each <=140 chars"],
  "impact": "1 sentence on why this matters to AI builders/researchers"
}
No prose outside the JSON. No code fences."""

USER_TEMPLATE = """Title: {title}
Source: {source}

Content:
{content}
"""


@dataclass
class Summary:
    model: str
    short: str
    bullets: list[str]
    impact: str | None


_JSON_RE = re.compile(r"\{.*\}", re.DOTALL)


def _extract_json(raw: str) -> dict:
    match = _JSON_RE.search(raw)
    if not match:
        raise ValueError(f"no JSON object found in model output: {raw[:200]}")
    return json.loads(match.group(0))


def summarize(*, title: str, source: str, content: str) -> Summary:
    provider = get_summary_provider()
    # Cap content to keep tokens predictable.
    snippet = (content or "")[:6000]
    raw = provider.complete(
        system=SYSTEM,
        user=USER_TEMPLATE.format(title=title, source=source, content=snippet),
        max_tokens=600,
        temperature=0.2,
    )
    data = _extract_json(raw)
    bullets = data.get("bullets") or []
    if not isinstance(bullets, list):
        bullets = []
    return Summary(
        model=f"{provider.name}:{provider.model}",
        short=(data.get("short") or "").strip(),
        bullets=[str(b).strip() for b in bullets if b],
        impact=(data.get("impact") or "").strip() or None,
    )
