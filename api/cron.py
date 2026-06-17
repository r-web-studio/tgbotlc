"""
Vercel serverless function entry point for cron/scheduled tasks.
Handles follow-up processing and other scheduled jobs.
"""
import os
import sys
import json
import asyncio
import logging
from http.server import BaseHTTPRequestHandler

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))

from dotenv import load_dotenv
load_dotenv()

from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.follow_up_repo import FollowUpRepository
from app.bot.services.notification_service import NotificationService
from app.utils.language import TRANSLATIONS

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def process_follow_ups() -> dict:
    """Process pending follow-up messages."""
    from app.config.settings import settings
    from aiogram import Bot
    from aiogram.client.default import DefaultBotProperties
    from aiogram.enums import ParseMode

    bot = Bot(
        token=settings.BOT_TOKEN,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    try:
        async with async_session() as session:
            follow_up_repo = FollowUpRepository(session)
            user_repo = UserRepository(session)
            pending = await follow_up_repo.get_pending()

            sent = 0
            failed = 0
            for follow_up in pending:
                try:
                    user = await user_repo.get_by_id(follow_up.user_id)
                    if not user:
                        logger.warning(f"User not found for follow-up {follow_up.id}, user_id={follow_up.user_id}")
                        await follow_up_repo.mark_failed(follow_up)
                        failed += 1
                        continue
                    await bot.send_message(user.telegram_id, follow_up.message)
                    await follow_up_repo.mark_sent(follow_up)
                    sent += 1
                    logger.info(f"Sent follow-up to user {user.telegram_id}")
                except Exception as e:
                    logger.error(f"Failed to send follow-up to user_id={follow_up.user_id}: {e}")
                    await follow_up_repo.mark_failed(follow_up)
                    failed += 1

            return {"status": "ok", "sent": sent, "failed": failed}
    finally:
        await bot.session.close()


class handler(BaseHTTPRequestHandler):
    """Vercel serverless function handler for cron tasks."""

    def do_GET(self):
        # Verify cron secret
        auth = self.headers.get("Authorization", "")
        from app.config.settings import settings
        if not auth or auth != f"Bearer {settings.SESSION_SECRET}":
            self.send_response(401)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Unauthorized"}).encode())
            return

        try:
            result = asyncio.run(process_follow_ups())
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            logger.error(f"Cron error: {e}")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def log_message(self, format, *args):
        pass
