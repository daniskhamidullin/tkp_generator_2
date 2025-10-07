from functools import lru_cache
from pathlib import Path
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    openai_api_key: Optional[str] = Field(default=None, env="OPENAI_API_KEY")
    openai_model: str = Field(default="gpt-5.1-mini", env="OPENAI_MODEL")
    project_name: str = "TKP Generator"
    schema_path: Path = Path(__file__).resolve().parent / "services" / "tkp_schema.json"
    templates_path: Path = Path(__file__).resolve().parent / "templates"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Return cached settings instance."""

    return Settings()


settings = get_settings()
