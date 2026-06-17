from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.user_repo import UserRepository
from app.bot.keyboards.reply import get_main_menu
from app.utils.language import TRANSLATIONS

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

    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    welcome_msg = t.get("welcome", "Welcome to Smart English Academy!")

    await message.answer(welcome_msg, reply_markup=get_main_menu(language))

@router.message(Command("help"))
async def cmd_help(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("help_text", "Available commands:\n/start - Start\n/help - Help\n/about - About\n/courses - Courses\n/contact - Contact"), reply_markup=get_main_menu(language))

@router.message(Command("about"))
async def cmd_about(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("about_text", "Smart English Academy offers IELTS, General English, Business English, and Kids English courses."), reply_markup=get_main_menu(language))
