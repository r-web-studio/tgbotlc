from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

class LanguageMiddleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]], event: TelegramObject, data: Dict[str, Any]) -> Any:
        from app.utils.language import detect_language

        if isinstance(event, Message) and event.text:
            lang = detect_language(event.text)
            data["language"] = lang
        else:
            data["language"] = "en"

        return await handler(event, data)
