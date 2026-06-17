from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_course_inline_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📖 IELTS Preparation", callback_data="course_ielts")],
        [InlineKeyboardButton(text="📖 General English", callback_data="course_general")],
        [InlineKeyboardButton(text="📖 Business English", callback_data="course_business")],
        [InlineKeyboardButton(text="📖 Kids English", callback_data="course_kids")],
    ])

def get_confirm_enroll_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✅ Confirm", callback_data="confirm_enroll")],
        [InlineKeyboardButton(text="❌ Cancel", callback_data="cancel_enroll")],
    ])
