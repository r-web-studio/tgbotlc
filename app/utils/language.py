from __future__ import annotations


def detect_language(text: str) -> str:
    if not text:
        return "en"

    text_lower = text.lower()
    total = len(text)
    if total == 0:
        return "en"

    cyrillic_count = sum(1 for ch in text if "\u0400" <= ch <= "\u04ff")
    cyrillic_ratio = cyrillic_count / total

    uz_specific = ["o'", "g'", "sh", "ch", "ya", "yu", "oʻ", "gʻ"]
    uz_hits = sum(1 for pattern in uz_specific if pattern in text_lower)

    if cyrillic_ratio > 0.5 and uz_hits >= 1:
        return "uz"
    if cyrillic_ratio > 0.5:
        return "ru"

    return "en"


TRANSLATIONS = {
    "en": {
        "welcome": "Welcome to our educational bot! Choose an option below:",
        "help_text": (
            "This bot helps you learn English, Russian, and Uzbek.\n\n"
            "📚 /courses - View available courses\n"
            "💰 /prices - Check pricing\n"
            "📍 /address - Our location\n"
            "📞 /contact - Contact us\n"
            "❓ /faq - Frequently asked questions\n"
            "📝 /enroll - Enroll in a course\n"
            "👤 /profile - Your profile"
        ),
        "courses_text": (
            "📚 Our Courses:\n\n"
            "1️⃣ General English - A1 to C2\n"
            "2️⃣ Business English - Professional communication\n"
            "3️⃣ IELTS Preparation - Score 7.0+\n"
            "4️⃣ Russian Language - Beginner to Advanced\n"
            "5️⃣ Uzbek Language - Native speaker courses\n\n"
            "To enroll, type /enroll"
        ),
        "prices_text": (
            "💰 Course Prices:\n\n"
            "📘 General English (Group) - $80/month\n"
            "📗 General English (Private) - $15/hour\n"
            "📙 Business English - $20/hour\n"
            "📕 IELTS Preparation - $25/hour\n"
            "📓 Russian Language - $12/hour\n"
            "📔 Uzbek Language - $10/hour\n\n"
            "All materials included!"
        ),
        "address_text": "📍 Our Address:\n123 Education Street, Tashkent, Uzbekistan\n\n🕐 Working Hours: Mon-Sat 9:00 - 20:00",
        "contact_text": "📞 Contact Us:\n\n📱 Phone: +998 90 123 45 67\n✉️ Email: info@edubot.uz\n💬 Telegram: @edubot_support",
        "faq_text": (
            "❓ Frequently Asked Questions:\n\n"
            "Q: What levels do you offer?\n"
            "A: We offer A1 to C2 levels.\n\n"
            "Q: How long is each course?\n"
            "A: 3-6 months depending on the level.\n\n"
            "Q: Do you offer trial lessons?\n"
            "A: Yes! First lesson is free."
        ),
        "enroll_start": "Great! Let's start your enrollment. What is your full name?",
        "ask_name": "Please enter your full name:",
        "ask_age": "How old are you?",
        "ask_phone": "Please enter your phone number (e.g., +998901234567):",
        "ask_level": "What is your current language level?\n\n1️⃣ Beginner (A1)\n2️⃣ Elementary (A2)\n3️⃣ Intermediate (B1)\n4️⃣ Upper-Intermediate (B2)\n5️⃣ Advanced (C1)\n6️⃣ Proficient (C2)",
        "ask_goal": "What is your learning goal?",
        "ask_time": "Preferred class time?\n\n1️⃣ Morning (9:00-12:00)\n2️⃣ Afternoon (12:00-17:00)\n3️⃣ Evening (17:00-20:00)",
        "enroll_complete": "✅ Enrollment submitted successfully! Our team will contact you soon.",
        "no_info": "Sorry, I don't have information on that. Please use the menu.",
        "error": "An error occurred. Please try again later.",
        "back_to_menu": "Back to Menu",
        "courses": "Courses",
        "prices": "Prices",
        "address": "Address",
        "contact": "Contact",
        "faq": "FAQ",
        "enroll": "Enroll",
    },
    "ru": {
        "welcome": "Добро пожаловать в наш образовательный бот! Выберите опцию:",
        "help_text": (
            "Этот бот помогает вам изучать английский, русский и узбекский языки.\n\n"
            "📚 /courses - Посмотреть курсы\n"
            "💰 /prices - Узнать цены\n"
            "📍 /address - Наш адрес\n"
            "📞 /contact - Связаться с нами\n"
            "❓ /faq - Часто задаваемые вопросы\n"
            "📝 /enroll - Записаться на курс\n"
            "👤 /profile - Ваш профиль"
        ),
        "courses_text": (
            "📚 Наши курсы:\n\n"
            "1️⃣ Английский язык - от A1 до C2\n"
            "2️⃣ Деловой английский - Профессиональное общение\n"
            "3️⃣ Подготовка к IELTS - Балл 7.0+\n"
            "4️⃣ Русский язык - От начального до продвинутого\n"
            "5️⃣ Узбекский язык - Курсы для носителей\n\n"
            "Для записи введите /enroll"
        ),
        "prices_text": (
            "💰 Стоимость курсов:\n\n"
            "📘 Английский (группа) - $80/мес\n"
            "📗 Английский (индивидуально) - $15/час\n"
            "📙 Деловой английский - $20/час\n"
            "📕 Подготовка к IELTS - $25/час\n"
            "📓 Русский язык - $12/час\n"
            "📔 Узбекский язык - $10/час\n\n"
            "Все материалы включены!"
        ),
        "address_text": "📍 Наш адрес:\nул. Образования 123, Ташкент, Узбекистан\n\n🕐 Часы работы: Пн-Сб 9:00 - 20:00",
        "contact_text": "📞 Свяжитесь с нами:\n\n📱 Телефон: +998 90 123 45 67\n✉️ Email: info@edubot.uz\n💬 Telegram: @edubot_support",
        "faq_text": (
            "❓ Часто задаваемые вопросы:\n\n"
            "В: Какие уровни вы предлагаете?\n"
            "О: Мы предлагаем уровни от A1 до C2.\n\n"
            "В: Сколько длится каждый курс?\n"
            "О: 3-6 месяцев в зависимости от уровня.\n\n"
            "В: Вы предлагаете пробные уроки?\n"
            "О: Да! Первый урок бесплатный."
        ),
        "enroll_start": "Отлично! Начнём запись. Как ваше полное имя?",
        "ask_name": "Пожалуйста, введите ваше полное имя:",
        "ask_age": "Сколько вам лет?",
        "ask_phone": "Введите номер телефона (напр., +998901234567):",
        "ask_level": "Какой у вас текущий уровень языка?\n\n1️⃣ Начинающий (A1)\n2️⃣ Элементарный (A2)\n3️⃣ Средний (B1)\n4️⃣ Выше среднего (B2)\n5️⃣ Продвинутый (C1)\n6️⃣ Свободный (C2)",
        "ask_goal": "Какова ваша цель обучения?",
        "ask_time": "Удобное время занятий?\n\n1️⃣ Утро (9:00-12:00)\n2️⃣ День (12:00-17:00)\n3️⃣ Вечер (17:00-20:00)",
        "enroll_complete": "✅ Запись успешно отправлена! Наша свяжется с вами в ближайшее время.",
        "no_info": "Извините, у меня нет информации по этому вопросу. Используйте меню.",
        "error": "Произошла ошибка. Пожалуйста, попробуйте позже.",
        "back_to_menu": "Back to Menu",
        "courses": "Courses",
        "prices": "Prices",
        "address": "Address",
        "contact": "Contact",
        "faq": "FAQ",
        "enroll": "Enroll",
    },
    "uz": {
        "welcome": "Bizning ta'lim botiga xush kelibsiz! Quyidagi variantni tanlang:",
        "help_text": (
            "Ushbu bot ingliz, rus va o'zbek tillarini o'rganishga yordam beradi.\n\n"
            "📚 /courses - Mavjud kurslar\n"
            "💰 /prices - Narxlarni ko'rish\n"
            "📍 /address - Manzilimiz\n"
            "📞 /contact - Bog'lanish\n"
            "❓ /faq - Ko'p beriladigan savollar\n"
            "📝 /enroll - Kursga yozilish\n"
            "👤 /profile - Sizning profilingiz"
        ),
        "courses_text": (
            "📚 Bizning kurslar:\n\n"
            "1️⃣ Umumiy ingliz tili - A1 dan C2 gacha\n"
            "2️⃣ Biznes ingliz tili - Kasbiy muloqot\n"
            "3️⃣ IELTSga tayyorlash - 7.0+ baho\n"
            "4️⃣ Rus tili - Boshlang'ichdan darajagacha\n"
            "5️⃣ O'zbek tili - Ona til kurslari\n\n"
            "Yozilish uchun /enroll buyrug'ini kiriting"
        ),
        "prices_text": (
            "💰 Kurs narxlari:\n\n"
            "📘 Umumiy ingliz tili (guruh) - $80/oy\n"
            "📗 Umumiy ingliz tili (shaxsiy) - $15/soat\n"
            "📙 Biznes ingliz tili - $20/soat\n"
            "📕 IELTSga tayyorlash - $25/soat\n"
            "📓 Rus tili - $12/soat\n"
            "📔 O'zbek tili - $10/soat\n\n"
            "Barcha materiallar kiritilgan!"
        ),
        "address_text": "📍 Manzilimiz:\nTa'lim ko'chasi 123, Toshkent, O'zbekiston\n\n🕐 Ish vaqti: Dush-San 9:00 - 20:00",
        "contact_text": "📞 Biz bilan bog'laning:\n\n📱 Telefon: +998 90 123 45 67\n✉️ Email: info@edubot.uz\n💬 Telegram: @edubot_support",
        "faq_text": (
            "❓ Ko'p beriladigan savollar:\n\n"
            "S: Qaysi darajalarni taklif qilasiz?\n"
            "J: Biz A1 dan C2 gacha darajalarni taklif qilamiz.\n\n"
            "S: Har bir kurs qancha vaqt davom etadi?\n"
            "J: Darajaga qarab 3-6 oy.\n\n"
            "S: Sinov darslari bormi?\n"
            "J: Ha! Birinchi dars bepul."
        ),
        "enroll_start": "Ajoyib! Yozilishni boshlaymiz. To'liq ismingiz nima?",
        "ask_name": "Iltimos, to'liq ismingizni kiriting:",
        "ask_age": "Yoshingiz nechada?",
        "ask_phone": "Telefon raqamingizni kiriting (masalan, +998901234567):",
        "ask_level": "Hozirgi tilingiz darajasi qanday?\n\n1️⃣ Boshlang'ich (A1)\n2️⃣ Elementar (A2)\n3️⃣ O'rta (B1)\n4️⃣ O'rtadan yuqori (B2)\n5️⃣ Yuqori (C1)\n6️⃣ Erkin (C2)",
        "ask_goal": "O'rganish maqsadingiz nima?",
        "ask_time": "Qulay dars vaqti?\n\n1️⃣ Ertalab (9:00-12:00)\n2️⃣ Kun (12:00-17:00)\n3️⃣ Kechqurun (17:00-20:00)",
        "enroll_complete": "✅ Yozilish muvaffaqiyatli yuborildi! Bizning jamoamiz siz bilan tez orada bog'lanadi.",
        "no_info": "Kechirasiz, bu haqda ma'lumotim yo'q. Iltimos, menyudan foydalaning.",
        "error": "Xatolik yuz berdi. Iltimos, keyinroq qayta urinib ko'ring.",
        "back_to_menu": "Back to Menu",
        "courses": "Courses",
        "prices": "Prices",
        "address": "Address",
        "contact": "Contact",
        "faq": "FAQ",
        "enroll": "Enroll",
    },
}


def get_translation(key: str, lang: str) -> str:
    lang_dict = TRANSLATIONS.get(lang, TRANSLATIONS.get("en", {}))
    return lang_dict.get(key, TRANSLATIONS.get("en", {}).get(key, key))
