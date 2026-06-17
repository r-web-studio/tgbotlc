from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.user_repo import UserRepository
from app.database.repositories.enrollment_repo import EnrollmentRepository
from app.database.repositories.lead_repo import LeadRepository
from app.bot.keyboards.reply import get_main_menu, get_level_keyboard, get_time_keyboard, get_back_keyboard
from app.utils.language import TRANSLATIONS as translations
from app.utils.validators import validate_phone, validate_age, sanitize_input
from app.config.settings import settings

router = Router()

class EnrollmentForm(StatesGroup):
    full_name = State()
    age = State()
    phone = State()
    english_level = State()
    goal = State()
    preferred_time = State()
    confirm = State()

async def send_to_admins(bot, text: str):
    for admin_id in settings.ADMIN_IDS:
        try:
            await bot.send_message(admin_id, text)
        except Exception:
            pass

@router.message(F.text.in_(["📝 Enroll", "📝 Записаться", "📝 Yozilish"]))
async def start_enrollment(message: Message, state: FSMContext, session: AsyncSession, language: str = "en"):
    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)
    if user:
        user.language = language
        await session.commit()

    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.full_name)
    await message.answer(t.get("ask_name", "Great! Let's get you enrolled. 📝\n\nWhat is your full name?"), reply_markup=get_back_keyboard(language))

@router.message(EnrollmentForm.full_name, F.text)
async def process_name(message: Message, state: FSMContext, session: AsyncSession, language: str = "en"):
    if message.text in ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    name = sanitize_input(message.text)
    await state.update_data(full_name=name)
    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.age)
    await message.answer(t.get("ask_age", "Nice to meet you, {}!\n\nHow old are you?".format(name)), reply_markup=get_back_keyboard(language))

@router.message(EnrollmentForm.age, F.text)
async def process_age(message: Message, state: FSMContext, language: str = "en"):
    if message.text in ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    if not validate_age(message.text):
        t = translations.get(language, translations["en"])
        await message.answer(t.get("invalid_age", "Please enter a valid age (10-80)."), reply_markup=get_back_keyboard(language))
        return

    await state.update_data(age=int(message.text))
    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.phone)
    await message.answer(t.get("ask_phone", "Thank you!\n\nPlease share your phone number:"), reply_markup=get_back_keyboard(language))

@router.message(EnrollmentForm.phone, F.text)
async def process_phone(message: Message, state: FSMContext, language: str = "en"):
    if message.text in ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    phone = sanitize_input(message.text)
    if not validate_phone(phone):
        t = translations.get(language, translations["en"])
        await message.answer(t.get("invalid_phone", "Please enter a valid phone number (e.g., +998901234567)."), reply_markup=get_back_keyboard(language))
        return

    await state.update_data(phone=phone)
    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.english_level)
    await message.answer(t.get("ask_level", "What is your current English level?"), reply_markup=get_level_keyboard(language))

@router.message(EnrollmentForm.english_level, F.text)
async def process_level(message: Message, state: FSMContext, language: str = "en"):
    back_texts = ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]
    if message.text in back_texts:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    valid_levels = ["A1 - Beginner", "A2 - Elementary", "B1 - Intermediate", "B2 - Upper-Intermediate", "C1 - Advanced",
                     "A1 - Начинающий", "A2 - Элементарный", "B1 - Средний", "B2 - Выше среднего", "C1 - Продвинутый",
                     "A1 - Boshlang'ich", "A2 - Oddiy", "B1 - O'rta", "B2 - O'rta Yuqori", "C1 - Yuqori"]

    level = message.text
    for vl in valid_levels:
        if message.text.split(" - ")[0].strip() == vl.split(" - ")[0].strip():
            level = vl.split(" - ")[0].strip()
            break

    await state.update_data(english_level=level)
    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.goal)
    await message.answer(t.get("ask_goal", "What is your goal for learning English?\n(e.g., IELTS, work, travel, general)"), reply_markup=get_back_keyboard(language))

@router.message(EnrollmentForm.goal, F.text)
async def process_goal(message: Message, state: FSMContext, language: str = "en"):
    if message.text in ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    await state.update_data(goal=sanitize_input(message.text))
    t = translations.get(language, translations["en"])
    await state.set_state(EnrollmentForm.preferred_time)
    await message.answer(t.get("ask_time", "When do you prefer to study?"), reply_markup=get_time_keyboard(language))

@router.message(EnrollmentForm.preferred_time, F.text)
async def process_time(message: Message, state: FSMContext, session: AsyncSession, language: str = "en"):
    if message.text in ["🔙 Back to Menu", "🔙 Назад в Меню", "🔙 Menyuga Qaytish"]:
        await state.clear()
        await message.answer("Main menu:", reply_markup=get_main_menu(language))
        return

    await state.update_data(preferred_time=sanitize_input(message.text))

    data = await state.get_data()
    t = translations.get(language, translations["en"])

    summary = t.get("enroll_summary", "📋 Please confirm your enrollment details:\n\n")
    summary += f"👤 Name: {data['full_name']}\n"
    summary += f"🎂 Age: {data['age']}\n"
    summary += f"📱 Phone: {data['phone']}\n"
    summary += f"📚 English Level: {data['english_level']}\n"
    summary += f"🎯 Goal: {data['goal']}\n"
    summary += f"🕐 Preferred Time: {data['preferred_time']}\n\n"
    summary += t.get("confirm_enroll", "Is everything correct?")

    await state.set_state(EnrollmentForm.confirm)
    from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
    from aiogram.utils.keyboard import ReplyKeyboardBuilder
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="✅ Confirm" if language == "en" else ("✅ Подтвердить" if language == "ru" else "✅ Tasdiqlash")),
                KeyboardButton(text="❌ Cancel" if language == "en" else ("❌ Отмена" if language == "ru" else "❌ Bekor qilish")))
    await message.answer(summary, reply_markup=builder.as_markup(resize_keyboard=True))

@router.message(EnrollmentForm.confirm, F.text)
async def process_confirm(message: Message, state: FSMContext, session: AsyncSession, language: str = "en"):
    confirm_texts = ["✅ Confirm", "✅ Подтвердить", "✅ Tasdiqlash"]
    cancel_texts = ["❌ Cancel", "❌ Отмена", "❌ Bekor qilish"]

    if message.text in cancel_texts:
        await state.clear()
        t = translations.get(language, translations["en"])
        await message.answer(t.get("enroll_cancelled", "Enrollment cancelled."), reply_markup=get_main_menu(language))
        return

    if message.text not in confirm_texts:
        return

    data = await state.get_data()

    user_repo = UserRepository(session)
    user = await user_repo.get_by_telegram_id(message.from_user.id)

    if user:
        await user_repo.update(user,
            full_name=data["full_name"],
            age=data["age"],
            phone=data["phone"],
            english_level=data["english_level"],
            goal=data["goal"],
            preferred_time=data["preferred_time"],
            is_enrolled=True,
            lead_status="enrolled"
        )

    enrollment_repo = EnrollmentRepository(session)
    enrollment = await enrollment_repo.create(
        user_id=user.id if user else 0,
        full_name=data["full_name"],
        age=data["age"],
        phone=data["phone"],
        english_level=data["english_level"],
        goal=data["goal"],
        preferred_time=data["preferred_time"]
    )

    lead_repo = LeadRepository(session)
    if user:
        await lead_repo.update_status(user.id, "enrolled", "Completed enrollment form")

    t = translations.get(language, translations["en"])
    await message.answer(t.get("enroll_complete", "🎉 Enrollment complete! We will contact you soon."), reply_markup=get_main_menu(language))

    username = f"@{user.username}" if user and user.username else "N/A"
    admin_msg = (
        f"🎉 New Enrollment!\n\n"
        f"👤 Name: {data['full_name']}\n"
        f"🎂 Age: {data['age']}\n"
        f"📱 Phone: {data['phone']}\n"
        f"📚 English Level: {data['english_level']}\n"
        f"🎯 Goal: {data['goal']}\n"
        f"🕐 Preferred Time: {data['preferred_time']}\n"
        f"💬 Telegram: {username}\n"
        f"🆔 User ID: {message.from_user.id}"
    )

    bot = message.bot
    if bot:
        await send_to_admins(bot, admin_msg)

    await state.clear()
