from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.user_repo import UserRepository
from app.bot.keyboards.reply import get_main_menu
from app.utils.language import TRANSLATIONS as translations

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message, session: AsyncSession, language: str = "en"):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if not user:
        user = await user_repo.create(
            telegram_id=message.from_user.id,
            username=message.from_user.username,
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            language=language
        )
    else:
        user.language = language
        await user_repo.update_last_interaction(user)

    t = translations.get(language, translations["en"])
    welcome_msg = t.get("welcome", "Welcome to Smart English Academy! 🎓\nI'm your AI educational consultant. How can I help you today?")

    await message.answer(welcome_msg, reply_markup=get_main_menu(language))

@router.message(Command("help"))
async def cmd_help(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("help_text", "Here are the available commands:\n/start - Start the bot\n/help - Show this message\n/about - About us\n/courses - Our courses\n/contact - Contact information"), reply_markup=get_main_menu(language))

@router.message(Command("about"))
async def cmd_about(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("about_text", "Smart English Academy is a leading language center offering IELTS preparation, General English, Business English, and Kids English courses."), reply_markup=get_main_menu(language))
