import asyncio
import logging
from datetime import datetime, timedelta
from aiogram import Bot
from app.database.engine import async_session
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.follow_up_repo import FollowUpRepository
from app.utils.language import TRANSLATIONS
from app.config.settings import settings

logger = logging.getLogger(__name__)

class Scheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.running = False
    
    async def start(self):
        self.running = True
        logger.info("Scheduler started")
        while self.running:
            try:
                await self.check_follow_ups()
                await self.check_inactive_users()
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
            await asyncio.sleep(3600)  # Check every hour
    
    async def stop(self):
        self.running = False
        logger.info("Scheduler stopped")
    
    async def check_follow_ups(self):
        async with async_session() as session:
            follow_up_repo = FollowUpRepository(session)
            user_repo = UserRepository(session)
            pending = await follow_up_repo.get_pending()
            
            for follow_up in pending:
                try:
                    user = await user_repo.get_by_id(follow_up.user_id)
                    if not user:
                        logger.warning(f"User not found for follow-up {follow_up.id}, user_id={follow_up.user_id}")
                        await follow_up_repo.mark_failed(follow_up)
                        continue
                    await self.bot.send_message(user.telegram_id, follow_up.message)
                    await follow_up_repo.mark_sent(follow_up)
                    logger.info(f"Sent follow-up to user {user.telegram_id}")
                except Exception as e:
                    logger.error(f"Failed to send follow-up to user_id={follow_up.user_id}: {e}")
                    await follow_up_repo.mark_failed(follow_up)
    
    async def check_inactive_users(self):
        async with async_session() as session:
            user_repo = UserRepository(session)
            follow_up_repo = FollowUpRepository(session)
            
            inactive_users = await user_repo.get_inactive_users(days=3)
            
            for user in inactive_users:
                has_pending = await follow_up_repo.has_pending_for_user(user.id)
                if has_pending:
                    continue
                
                lang = user.language or "en"
                t = TRANSLATIONS.get(lang, TRANSLATIONS.get("en", {}))
                message = t.get("follow_up", "Hello! You were interested in our English courses. If you still have questions, I'll be happy to help!")
                
                scheduled_at = datetime.utcnow()
                await follow_up_repo.create(user.id, message, scheduled_at)
                logger.info(f"Scheduled follow-up for user {user.id}")
    
    async def schedule_follow_up(self, user_id: int, message: str, delay_hours: int = 72):
        async with async_session() as session:
            follow_up_repo = FollowUpRepository(session)
            scheduled_at = datetime.utcnow() + timedelta(hours=delay_hours)
            await follow_up_repo.create(user_id, message, scheduled_at)
