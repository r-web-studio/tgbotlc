import pytest
import os
from unittest.mock import patch

class TestConfig:
    def test_settings_load(self):
        with patch.dict(os.environ, {
            "BOT_TOKEN": "test_token",
            "OPENROUTER_API_KEY": "test_key",
            "DATABASE_URL": "postgresql+asyncpg://test:test@localhost/test",
            "ADMIN_IDS": "123,456",
            "ADMIN_USERNAME": "admin",
            "ADMIN_PASSWORD": "password",
            "SESSION_SECRET": "secret"
        }):
            from app.config.settings import Settings
            settings = Settings()
            assert settings.BOT_TOKEN == "test_token"
            assert settings.OPENROUTER_API_KEY == "test_key"
            assert settings.ADMIN_IDS == [123, 456]
