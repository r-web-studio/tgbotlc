from __future__ import annotations

from typing import Any


def format_user_profile(user: dict[str, Any]) -> str:
    name = user.get("full_name", "N/A")
    age = user.get("age", "N/A")
    phone = user.get("phone", "N/A")
    level = user.get("language_level", "N/A")
    goal = user.get("learning_goal", "N/A")
    preferred_time = user.get("preferred_time", "N/A")
    telegram_id = user.get("telegram_id", "N/A")
    created = user.get("created_at", "N/A")

    return (
        f"👤 User Profile\n"
        f"{'─' * 24}\n"
        f"🆔 Telegram ID: {telegram_id}\n"
        f"📛 Name: {name}\n"
        f"🎂 Age: {age}\n"
        f"📱 Phone: {phone}\n"
        f"📚 Level: {level}\n"
        f"🎯 Goal: {goal}\n"
        f"🕐 Preferred Time: {preferred_time}\n"
        f"📅 Registered: {created}"
    )


def format_enrollment(enrollment: dict[str, Any]) -> str:
    user_name = enrollment.get("user_name", "N/A")
    course = enrollment.get("course", "N/A")
    level = enrollment.get("level", "N/A")
    preferred_time = enrollment.get("preferred_time", "N/A")
    phone = enrollment.get("phone", "N/A")
    status = enrollment.get("status", "pending")
    created = enrollment.get("created_at", "N/A")

    status_emoji = {
        "pending": "🟡",
        "approved": "🟢",
        "rejected": "🔴",
        "completed": "🔵",
    }.get(status, "⚪")

    return (
        f"📝 Enrollment Details\n"
        f"{'─' * 24}\n"
        f"👤 Student: {user_name}\n"
        f"📘 Course: {course}\n"
        f"📚 Level: {level}\n"
        f"🕐 Time: {preferred_time}\n"
        f"📱 Phone: {phone}\n"
        f"📊 Status: {status_emoji} {status.capitalize()}\n"
        f"📅 Date: {created}"
    )


def format_admin_notification(data: dict[str, Any]) -> str:
    name = data.get("full_name", "N/A")
    age = data.get("age", "N/A")
    phone = data.get("phone", "N/A")
    level = data.get("language_level", "N/A")
    goal = data.get("learning_goal", "N/A")
    preferred_time = data.get("preferred_time", "N/A")
    telegram_id = data.get("telegram_id", "N/A")
    username = data.get("username", "")

    username_str = f"@{username}" if username else "N/A"

    return (
        f"🆕 New Enrollment Request!\n"
        f"{'═' * 26}\n"
        f"🆔 Telegram ID: {telegram_id}\n"
        f"📛 Name: {name}\n"
        f"👤 Username: {username_str}\n"
        f"🎂 Age: {age}\n"
        f"📱 Phone: {phone}\n"
        f"📚 Level: {level}\n"
        f"🎯 Goal: {goal}\n"
        f"🕐 Preferred Time: {preferred_time}\n"
        f"{'═' * 26}\n"
        f"Use the admin panel to approve or reject."
    )
