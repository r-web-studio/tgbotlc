from __future__ import annotations

import re
import html


def validate_phone(phone: str) -> bool:
    phone = phone.strip()
    if not phone.startswith("+"):
        return False
    digits = phone[1:]
    if not digits.isdigit():
        return False
    return 10 <= len(digits) <= 15


def validate_age(age: str) -> bool:
    try:
        value = int(age.strip())
    except (ValueError, TypeError):
        return False
    return 10 <= value <= 80


def sanitize_input(text: str) -> str:
    text = text.strip()
    text = html.escape(text)
    text = re.sub(r"<script[^>]*>.*?</script>", "", text, flags=re.IGNORECASE | re.DOTALL)
    text = re.sub(r"javascript:", "", text, flags=re.IGNORECASE)
    text = re.sub(r"on\w+\s*=", "", text, flags=re.IGNORECASE)
    if len(text) > 2000:
        text = text[:2000]
    return text
