from __future__ import annotations

import json
from pydantic import model_validator
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

    @model_validator(mode="before")
    @classmethod
    def parse_admin_ids(cls, data: dict) -> dict:
        raw = data.get("ADMIN_IDS")
        if raw is None:
            data["ADMIN_IDS"] = []
            return data
        if isinstance(raw, list):
            return data
        if isinstance(raw, int):
            data["ADMIN_IDS"] = [raw]
            return data
        if isinstance(raw, str):
            raw = raw.strip()
            if not raw:
                data["ADMIN_IDS"] = []
                return data
            # Try JSON array: "[1234, 5678]"
            if raw.startswith("["):
                try:
                    parsed = json.loads(raw)
                    if isinstance(parsed, list):
                        data["ADMIN_IDS"] = [int(x) for x in parsed]
                        return data
                except (json.JSONDecodeError, ValueError):
                    pass
            # Comma-separated or single
            parts = [p.strip() for p in raw.split(",")]
            result = []
            for part in parts:
                if part.isdigit():
                    result.append(int(part))
            data["ADMIN_IDS"] = result
            return data
        data["ADMIN_IDS"] = []
        return data


settings = Settings()
