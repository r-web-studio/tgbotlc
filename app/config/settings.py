from __future__ import annotations

import json
from pydantic import field_validator
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
    ADMIN_IDS: list[int] = []
    ADMIN_USERNAME: str = ""
    ADMIN_PASSWORD: str = ""
    SESSION_SECRET: str = "change-me-in-production"

    @field_validator("ADMIN_IDS", mode="before")
    @classmethod
    def parse_admin_ids(cls, v):
        if isinstance(v, list):
            return v
        if isinstance(v, int):
            return [v]
        if isinstance(v, str):
            v = v.strip()
            if not v:
                return []
            if v.startswith("["):
                try:
                    parsed = json.loads(v)
                    if isinstance(parsed, list):
                        return [int(x) for x in parsed]
                except (json.JSONDecodeError, ValueError):
                    pass
            parts = [p.strip() for p in v.split(",")]
            result = []
            for part in parts:
                if part.isdigit():
                    result.append(int(part))
            return result
        return []


settings = Settings()
