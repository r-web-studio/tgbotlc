from aiogram import Router, F
from aiogram.types import Message
from app.bot.keyboards.reply import get_main_menu
from app.utils.language import TRANSLATIONS

router = Router()

@router.message(F.text.in_(["📚 Courses", "📚 Курсы", "📚 Kurslar"]))
async def courses_handler(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("courses_text", "We offer IELTS, General, Business English, and Kids courses."), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["💰 Prices", "💰 Цены", "💰 Narxlar"]))
async def prices_handler(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("prices_text", "Course prices available on request."), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["📍 Address", "📍 Адрес", "📍 Manzil"]))
async def address_handler(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("address_text", "123 Education Street, Tashkent"), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["📞 Contact", "📞 Контакт", "📞 Aloqa"]))
async def contact_handler(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("contact_text", "Phone: +998 90 123 45 67"), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["❓ FAQ", "❓ Вопросы", "❓ Savollar"]))
async def faq_handler(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("faq_text", "Frequently asked questions."), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]))
async def back_to_menu(message: Message, language: str = "en"):
    t = TRANSLATIONS.get(language, TRANSLATIONS.get("en", {}))
    await message.answer(t.get("welcome", "Welcome!"), reply_markup=get_main_menu(language))
