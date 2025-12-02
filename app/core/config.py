"""Centralizovana konfiguracija za customer assistant bot."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic import HttpUrl, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

Llms = Literal["openai", "ollama", "bedrock", "sagemaker"]


class Settings(BaseSettings):
    """Projicira konfiguraciju iz `.env` i sistemskih promenljivih."""

    app_environment: str = "local"
    knowledge_base_path: Path = Path("data/policies")
    vector_store_path: Path = Path("data/vector_store")

    order_service_url: Optional[HttpUrl] = None
    order_service_api_key: Optional[str] = None
    inventory_service_url: Optional[HttpUrl] = None
    billing_service_url: Optional[HttpUrl] = None
    shipment_service_url: Optional[HttpUrl] = None

    default_llm_provider: Llms = "ollama"
    openai_api_key: Optional[str] = None
    ollama_model: str = "mistral"
    bedrock_model_id: Optional[str] = None
    aws_profile: Optional[str] = None

    embedding_model_name: str = "nomic-embed-text"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("openai_api_key", mode="before")
    @classmethod
    def _strip_empty(cls, value: Optional[str]) -> Optional[str]:
        if value == "":
            return None
        return value


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Vraća keširani Settings objekat."""

    return Settings()


__all__ = ["Settings", "get_settings"]
