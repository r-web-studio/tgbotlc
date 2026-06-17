from __future__ import annotations

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    BOT_TOKEN: str = ""
    OPENROUTER_API_KEY: str = ""
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/edubot"
    ADMIN_IDS: list[int] = Field(default_factory=list)
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""
    SESSION_SECRET: str = "change-me-in-production"

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v: str | list[int] | None) -> list[int]:
        if isinstance(v, list):
            return v
        if isinstance(v, str) and v.strip():
            return [int(x.strip()) for x in v.split(",") if x.strip().isdigit()]
        return []


settings = Settings()
