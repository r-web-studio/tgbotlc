from __future__ import annotations

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
    def parse_admin_ids(cls, values: dict) -> dict:
        if "ADMIN_IDS" in values:
            raw = values["ADMIN_IDS"]
            if isinstance(raw, list):
                values["ADMIN_IDS"] = raw
            elif isinstance(raw, str) and raw.strip():
                values["ADMIN_IDS"] = [
                    int(x.strip()) for x in raw.split(",") if x.strip().isdigit()
                ]
            else:
                values["ADMIN_IDS"] = []
        return values


settings = Settings()
