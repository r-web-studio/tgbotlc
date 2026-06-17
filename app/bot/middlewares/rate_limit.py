import time
from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message

class RateLimitMiddleware(BaseMiddleware):
    def __init__(self, limit: int = 1, period: float = 60.0):
        self.limit = limit
        self.period = period
        self.user_timestamps: Dict[int, list] = {}
        self._cleanup_interval = 300  # cleanup every 5 minutes
        self._last_cleanup = time.time()

    def _cleanup_stale_users(self):
        """Remove users with no recent timestamps to prevent memory leak."""
        now = time.time()
        if now - self._last_cleanup < self._cleanup_interval:
            return
        self._last_cleanup = now
        stale_keys = [
            uid for uid, timestamps in self.user_timestamps.items()
            if not timestamps or all(now - t >= self.period for t in timestamps)
        ]
        for uid in stale_keys:
            del self.user_timestamps[uid]

    async def __call__(self, handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]], event: Message, data: Dict[str, Any]) -> Any:
        user_id = event.from_user.id
        now = time.time()

        self._cleanup_stale_users()

        if user_id not in self.user_timestamps:
            self.user_timestamps[user_id] = []

        self.user_timestamps[user_id] = [t for t in self.user_timestamps[user_id] if now - t < self.period]

        if len(self.user_timestamps[user_id]) >= self.limit:
            from app.utils.language import TRANSLATIONS as translations
            lang = data.get("language", "en")
            msg = translations.get(lang, translations["en"]).get("rate_limit", "Please wait a moment before sending another message.")
            await event.answer(msg)
            return None

        self.user_timestamps[user_id].append(now)
        return await handler(event, data)
