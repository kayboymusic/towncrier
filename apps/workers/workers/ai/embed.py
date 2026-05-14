from __future__ import annotations

from workers.ai.llm import get_openai_client
from workers.config import settings


def embed(text: str) -> list[float]:
    """Return a single embedding for the given text."""
    client = get_openai_client()
    snippet = (text or "")[:8000]
    resp = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=snippet,
    )
    return resp.data[0].embedding


def embed_batch(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []
    client = get_openai_client()
    snippets = [(t or "")[:8000] for t in texts]
    resp = client.embeddings.create(
        model=settings.openai_embedding_model,
        input=snippets,
    )
    return [d.embedding for d in resp.data]
