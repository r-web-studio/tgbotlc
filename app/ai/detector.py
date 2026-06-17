import re
from typing import Optional


class IntentDetector:
    INTENTS = {
        "greeting": ["hello", "hi", "hey", "salam", "привет", "ассалому"],
        "courses": ["course", "kurs", "курс", "program", "программа"],
        "price": ["price", "cost", "narx", "цена", "стоимость", "how much"],
        "enrollment": [
            "enroll",
            "register",
            "sign up",
            "записаться",
            "зарегистрироваться",
            "ypo'zish",
            "ro'yxatdan",
        ],
        "schedule": ["schedule", "time", "when", "расписание", "время", "жадвал"],
        "address": ["address", "location", "where", "адрес", "где", "manzil"],
        "contact": ["phone", "contact", "tel", "телефон", "контакт"],
        "faq": ["question", "help", "вопрос", "помощь"],
        "goodbye": ["bye", "goodbye", "see you", "пока", "до свидания", "хайр"],
        "thanks": ["thank", "thanks", "спасибо", "rahmat"],
    }

    LEAD_SIGNALS = {
        "hot": [
            "enroll",
            "register",
            "sign up",
            "записаться",
            "want to join",
            "хочу записаться",
            "how to enroll",
        ],
        "warm": [
            "price",
            "cost",
            "more info",
            "tell me about",
            "цена",
            "подробнее",
            "narx",
        ],
        "cold": ["just looking", "just curious", "просто смотрю"],
    }

    @classmethod
    def detect_intent(cls, text: str) -> str:
        text_lower = text.lower().strip()
        scores = {}
        for intent, keywords in cls.INTENTS.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            if score > 0:
                scores[intent] = score
        if scores:
            return max(scores, key=scores.get)
        return "general"

    @classmethod
    def detect_lead_signal(cls, text: str) -> Optional[str]:
        text_lower = text.lower().strip()
        for level, signals in cls.LEAD_SIGNALS.items():
            for signal in signals:
                if signal in text_lower:
                    return level
        return None

    @classmethod
    def should_suggest_enrollment(cls, text: str, user_info: dict) -> bool:
        text_lower = text.lower().strip()
        enrollment_signals = [
            "yes",
            "sure",
            "interested",
            "да",
            "хочу",
            "interested",
            "okay",
            "ok",
        ]
        has_basic_info = all(
            user_info.get(k) for k in ["full_name", "phone", "english_level"]
        )
        signals_found = any(s in text_lower for s in enrollment_signals)
        return signals_found and has_basic_info
