from aiogram import Bot
from app.config.settings import settings
import logging

logger = logging.getLogger(__name__)

class NotificationService:
    def __init__(self, bot: Bot):
        self.bot = bot
    
    async def notify_admins(self, message: str) -> list[int]:
        sent_to = []
        for admin_id in settings.ADMIN_IDS:
            try:
                await self.bot.send_message(admin_id, message)
                sent_to.append(admin_id)
            except Exception as e:
                logger.error(f"Failed to notify admin {admin_id}: {e}")
        return sent_to
    
    async def notify_enrollment(self, enrollment_data: dict) -> list[int]:
        username = enrollment_data.get("username", "N/A")
        if username and username != "N/A":
            username = f"@{username}"
        
        message = (
            "🎉 *New Enrollment!*\n\n"
            f"👤 Name: {enrollment_data.get('full_name', 'N/A')}\n"
            f"🎂 Age: {enrollment_data.get('age', 'N/A')}\n"
            f"📱 Phone: {enrollment_data.get('phone', 'N/A')}\n"
            f"📚 English Level: {enrollment_data.get('english_level', 'N/A')}\n"
            f"🎯 Goal: {enrollment_data.get('goal', 'N/A')}\n"
            f"🕐 Preferred Time: {enrollment_data.get('preferred_time', 'N/A')}\n"
            f"💬 Telegram: {username}\n"
            f"🆔 User ID: {enrollment_data.get('telegram_id', 'N/A')}"
        )
        
        return await self.notify_admins(message)
    
    async def notify_lead_update(self, user_data: dict, old_status: str, new_status: str) -> list[int]:
        message = (
            "📊 *Lead Status Updated*\n\n"
            f"👤 User: {user_data.get('full_name', 'N/A')} (@{user_data.get('username', 'N/A')})\n"
            f"📈 Status: {old_status} → {new_status}\n"
            f"🆔 User ID: {user_data.get('telegram_id', 'N/A')}"
        )
        return await self.notify_admins(message)
