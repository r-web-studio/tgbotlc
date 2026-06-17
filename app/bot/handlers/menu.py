from aiogram import Router, F
from aiogram.types import Message
from app.bot.keyboards.reply import get_main_menu
from app.utils.language import TRANSLATIONS as translations

router = Router()

@router.message(F.text.in_(["📚 Courses", "📚 Курсы", "📚 Kurslar"]))
async def courses_handler(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("courses_text", "We offer:\n\n📖 IELTS Preparation\n📖 General English\n📖 Business English\n📖 Kids English\n\nSelect a course for more details!"), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["💰 Prices", "💰 Цены", "💰 Narxlar"]))
async def prices_handler(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("prices_text", "Our course prices:\n\n📖 IELTS Preparation: $500\n📖 General English: $300\n📖 Business English: $400\n📖 Kids English: $250\n\nPrices may vary by schedule."), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["📍 Address", "📍 Адрес", "📍 Manzil"]))
async def address_handler(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("address_text", "📍 Our Address:\n\n123 Education Street\nTashkent, Uzbekistan\n\nMon-Sat: 9:00 AM - 8:00 PM"), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["📞 Contact", "📞 Контакт", "📞 Aloqa"]))
async def contact_handler(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("contact_text", "📞 Contact Us:\n\n📱 Phone: +998 90 123 45 67\n📧 Email: info@smartenglish.uz\n💬 Telegram: @smartenglish\n\nFeel free to reach out!"), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["❓ FAQ", "❓ Вопросы", "❓ Savollar"]))
async def faq_handler(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("faq_text", "❓ Frequently Asked Questions:\n\n1. Do I need prior English knowledge?\n - We have courses for all levels!\n\n2. Can I get a trial lesson?\n - Yes! Contact us for a free trial.\n\n3. What are the class sizes?\n - Small groups of 5-10 students.\n\n4. Do you offer certificates?\n - Yes, certificates are provided upon completion."), reply_markup=get_main_menu(language))

@router.message(F.text.in_(["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]))
async def back_to_menu(message: Message, language: str = "en"):
    t = translations.get(language, translations["en"])
    await message.answer(t.get("welcome", "Welcome! How can I help you?"), reply_markup=get_main_menu(language))
