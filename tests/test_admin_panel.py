import pytest
from app.admin_panel.auth import hash_password, verify_password, create_session_token, validate_session_token

class TestAdminAuth:
    def test_hash_password(self):
        hashed = hash_password("test123")
        assert hashed != "test123"
        assert len(hashed) == 64  # SHA256 hex digest

    def test_verify_password(self):
        hashed = hash_password("mypassword")
        assert verify_password("mypassword", hashed) is True
        assert verify_password("wrongpassword", hashed) is False

    def test_session_token(self):
        token = create_session_token("admin")
        data = validate_session_token(token)
        assert data is not None
        assert data["admin_id"] == "admin"

    def test_invalid_token(self):
        data = validate_session_token("invalid_token")
        assert data is None
