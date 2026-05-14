"""Provider-agnostic LLM interface.

Three concrete providers: Anthropic Claude, OpenAI, and xAI Grok.
Grok exposes an OpenAI-compatible chat completions API, so we reuse
the OpenAI SDK pointed at api.x.ai for it.

Embeddings always use OpenAI — only OpenAI ships a high-quality,
affordable embedding endpoint we want to depend on today.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from functools import lru_cache

from anthropic import Anthropic
from openai import OpenAI

from workers.config import Provider, settings


class LLMProvider(ABC):
    name: Provider

    @abstractmethod
    def complete(self, *, system: str, user: str, max_tokens: int = 1024, temperature: float = 0.2) -> str:
        """Return assistant text for a single-turn prompt."""


class AnthropicProvider(LLMProvider):
    name: Provider = "anthropic"

    def __init__(self, model: str | None = None) -> None:
        if not settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY is not set")
        self._client = Anthropic(api_key=settings.anthropic_api_key)
        self.model = model or settings.anthropic_summary_model

    def complete(self, *, system: str, user: str, max_tokens: int = 1024, temperature: float = 0.2) -> str:
        msg = self._client.messages.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system,
            messages=[{"role": "user", "content": user}],
        )
        # Concatenate any text blocks.
        parts: list[str] = []
        for block in msg.content:
            if getattr(block, "type", None) == "text":
                parts.append(block.text)
        return "".join(parts).strip()


class OpenAIProvider(LLMProvider):
    name: Provider = "openai"

    def __init__(self, model: str | None = None) -> None:
        if not settings.openai_api_key:
            raise RuntimeError("OPENAI_API_KEY is not set")
        self._client = OpenAI(api_key=settings.openai_api_key)
        self.model = model or settings.openai_summary_model

    def complete(self, *, system: str, user: str, max_tokens: int = 1024, temperature: float = 0.2) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return (resp.choices[0].message.content or "").strip()


class GrokProvider(LLMProvider):
    """xAI Grok via OpenAI-compatible endpoint."""

    name: Provider = "grok"

    def __init__(self, model: str | None = None) -> None:
        if not settings.xai_api_key:
            raise RuntimeError("XAI_API_KEY is not set")
        self._client = OpenAI(api_key=settings.xai_api_key, base_url="https://api.x.ai/v1")
        self.model = model or settings.grok_model

    def complete(self, *, system: str, user: str, max_tokens: int = 1024, temperature: float = 0.2) -> str:
        resp = self._client.chat.completions.create(
            model=self.model,
            max_tokens=max_tokens,
            temperature=temperature,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
        )
        return (resp.choices[0].message.content or "").strip()


@lru_cache(maxsize=8)
def get_provider(name: Provider, model: str | None = None) -> LLMProvider:
    if name == "anthropic":
        return AnthropicProvider(model)
    if name == "openai":
        return OpenAIProvider(model)
    if name == "grok":
        return GrokProvider(model)
    raise ValueError(f"unknown provider: {name}")


def get_summary_provider() -> LLMProvider:
    return get_provider(settings.summary_provider)


def get_classify_provider() -> LLMProvider:
    model = (
        settings.anthropic_classify_model
        if settings.classify_provider == "anthropic"
        else None
    )
    return get_provider(settings.classify_provider, model)


@lru_cache(maxsize=1)
def get_openai_client() -> OpenAI:
    """Dedicated OpenAI client for embeddings — always OpenAI."""
    if not settings.openai_api_key:
        raise RuntimeError("OPENAI_API_KEY is required for embeddings")
    return OpenAI(api_key=settings.openai_api_key)
