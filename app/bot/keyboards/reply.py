from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

def get_main_menu(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": {"courses": "📚 Courses", "prices": "💰 Prices", "address": "📍 Address", "contact": "📞 Contact", "enroll": "📝 Enroll", "faq": "❓ FAQ"},
        "ru": {"courses": "📚 Курсы", "prices": "💰 Цены", "address": "📍 Адрес", "contact": "📞 Контакт", "enroll": "📝 Записаться", "faq": "❓ Вопросы"},
        "uz": {"courses": "📚 Kurslar", "prices": "💰 Narxlar", "address": "📍 Manzil", "contact": "📞 Aloqa", "enroll": "📝 Yozilish", "faq": "❓ Savollar"},
    }
    t = translations.get(language, translations["en"])
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t["courses"]), KeyboardButton(text=t["prices"]))
    builder.row(KeyboardButton(text=t["address"]), KeyboardButton(text=t["contact"]))
    builder.row(KeyboardButton(text=t["enroll"]), KeyboardButton(text=t["faq"]))
    return builder.as_markup(resize_keyboard=True)

def get_contact_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": {"phone": "📱 Share Phone", "back": "🔙 Back"},
        "ru": {"phone": "📱 Отправить Телефон", "back": "🔙 Назад"},
        "uz": {"phone": "📱 Telefon Yuborish", "back": "🔙 Orqaga"},
    }
    t = translations.get(language, translations["en"])
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t["phone"], request_contact=True))
    builder.row(KeyboardButton(text=t["back"]))
    return builder.as_markup(resize_keyboard=True)

def get_confirm_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": {"yes": "✅ Yes", "no": "❌ No"},
        "ru": {"yes": "✅ Да", "no": "❌ Нет"},
        "uz": {"yes": "✅ Ha", "no": "❌ Yo'q"},
    }
    t = translations.get(language, translations["en"])
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t["yes"]), KeyboardButton(text=t["no"]))
    return builder.as_markup(resize_keyboard=True)

def get_back_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": "🔙 Back to Menu",
        "ru": "🔙 Назад в Меню",
        "uz": "🔙 Menyuga Qaytish",
    }
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=translations.get(language, translations["en"])))
    return builder.as_markup(resize_keyboard=True)

def get_level_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": {"a1": "A1 - Beginner", "a2": "A2 - Elementary", "b1": "B1 - Intermediate", "b2": "B2 - Upper-Intermediate", "c1": "C1 - Advanced", "back": "🔙 Back"},
        "ru": {"a1": "A1 - Начинающий", "a2": "A2 - Элементарный", "b1": "B1 - Средний", "b2": "B2 - Выше среднего", "c1": "C1 - Продвинутый", "back": "🔙 Назад"},
        "uz": {"a1": "A1 - Boshlang'ich", "a2": "A2 - Oddiy", "b1": "B1 - O'rta", "b2": "B2 - O'rta Yuqori", "c1": "C1 - Yuqori", "back": "🔙 Orqaga"},
    }
    t = translations.get(language, translations["en"])
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t["a1"]), KeyboardButton(text=t["a2"]))
    builder.row(KeyboardButton(text=t["b1"]), KeyboardButton(text=t["b2"]))
    builder.row(KeyboardButton(text=t["c1"]))
    builder.row(KeyboardButton(text=t["back"]))
    return builder.as_markup(resize_keyboard=True)

def get_time_keyboard(language: str = "en") -> ReplyKeyboardMarkup:
    translations = {
        "en": {"morning": "🌅 Morning (9:00-12:00)", "afternoon": "☀️ Afternoon (13:00-16:00)", "evening": "🌙 Evening (17:00-20:00)", "flexible": "🕐 Flexible", "back": "🔙 Back"},
        "ru": {"morning": "🌅 Утро (9:00-12:00)", "afternoon": "☀️ День (13:00-16:00)", "evening": "🌙 Вечер (17:00-20:00)", "flexible": "🕐 Гибкое", "back": "🔙 Назад"},
        "uz": {"morning": "🌅 Ertalab (9:00-12:00)", "afternoon": "☀️ Kunduzi (13:00-16:00)", "evening": "🌙 Kechqurun (17:00-20:00)", "flexible": "🕐 Mos", "back": "🔙 Orqaga"},
    }
    t = translations.get(language, translations["en"])
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t["morning"]), KeyboardButton(text=t["afternoon"]))
    builder.row(KeyboardButton(text=t["evening"]), KeyboardButton(text=t["flexible"]))
    builder.row(KeyboardButton(text=t["back"]))
    return builder.as_markup(resize_keyboard=True)
