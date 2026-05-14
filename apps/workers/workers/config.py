from __future__ import annotations

from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

REPO_ROOT = Path(__file__).resolve().parents[3]
ENV_FILE = REPO_ROOT / ".env"

Provider = Literal["anthropic", "openai", "grok"]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(ENV_FILE),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    supabase_url: str = ""
    supabase_service_role_key: str = ""
    database_url: str = ""

    anthropic_api_key: str = ""
    openai_api_key: str = ""
    xai_api_key: str = ""

    summary_provider: Provider = "anthropic"
    classify_provider: Provider = "anthropic"

    anthropic_summary_model: str = "claude-sonnet-4-6"
    anthropic_classify_model: str = "claude-haiku-4-5-20251001"
    openai_summary_model: str = "gpt-4o-mini"
    openai_embedding_model: str = "text-embedding-3-small"
    grok_model: str = "grok-4"

    dedup_similarity_threshold: float = 0.92
    dedup_lookback_days: int = 7

    log_level: str = "INFO"


settings = Settings()
