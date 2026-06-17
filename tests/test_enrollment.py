import pytest
from app.utils.validators import validate_phone, validate_age, sanitize_input

class TestValidators:
    def test_valid_phone(self):
        assert validate_phone("+998901234567") is True
        assert validate_phone("+1234567890") is True
        assert validate_phone("998901234567") is True

    def test_invalid_phone(self):
        assert validate_phone("123") is False
        assert validate_phone("abc") is False
        assert validate_phone("") is False

    def test_valid_age(self):
        assert validate_age("15") is True
        assert validate_age("25") is True
        assert validate_age("70") is True

    def test_invalid_age(self):
        assert validate_age("5") is False
        assert validate_age("100") is False
        assert validate_age("abc") is False
        assert validate_age("") is False

    def test_sanitize_input(self):
        assert sanitize_input("  Hello  ") == "Hello"
        assert sanitize_input("Test<script>alert('xss')</script>") != "Test<script>alert('xss')</script>"
        assert len(sanitize_input("a" * 3000)) <= 2000

class TestEnrollmentFlow:
    def test_enrollment_states(self):
        from app.bot.handlers.enrollment import EnrollmentForm
        assert EnrollmentForm.full_name is not None
        assert EnrollmentForm.age is not None
        assert EnrollmentForm.phone is not None
        assert EnrollmentForm.english_level is not None
        assert EnrollmentForm.goal is not None
        assert EnrollmentForm.preferred_time is not None
        assert EnrollmentForm.confirm is not None
