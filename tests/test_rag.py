import pytest
from app.rag.chain import chunk_text
from app.ai.detector import IntentDetector

class TestChunking:
    def test_chunk_text(self):
        text = "A" * 1000
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        assert len(chunks) > 0
        assert all(len(c) <= 250 for c in chunks)

    def test_chunk_text_small(self):
        text = "Hello world"
        chunks = chunk_text(text, chunk_size=200, overlap=50)
        assert len(chunks) == 1
        assert chunks[0] == "Hello world"

    def test_chunk_text_empty(self):
        chunks = chunk_text("", chunk_size=200, overlap=50)
        assert len(chunks) == 0

class TestIntentDetector:
    def test_detect_greeting(self):
        assert IntentDetector.detect_intent("Hello!") == "greeting"
        assert IntentDetector.detect_intent("Привет!") == "greeting"
        assert IntentDetector.detect_intent("Assalomu alaykum") == "greeting"

    def test_detect_courses(self):
        assert IntentDetector.detect_intent("Tell me about courses") == "courses"
        assert IntentDetector.detect_intent("Какие курсы есть?") == "courses"

    def test_detect_price(self):
        assert IntentDetector.detect_intent("How much does it cost?") == "price"
        assert IntentDetector.detect_intent("Сколько стоит?") == "price"

    def test_detect_enrollment(self):
        assert IntentDetector.detect_intent("I want to enroll") == "enrollment"
        assert IntentDetector.detect_intent("Записаться на курс") == "enrollment"

    def test_detect_lead_signals(self):
        assert IntentDetector.detect_lead_signal("I want to enroll now") == "hot"
        assert IntentDetector.detect_lead_signal("What's the price?") == "warm"
        assert IntentDetector.detect_lead_signal("Just looking") == "cold"
        assert IntentDetector.detect_lead_signal("Nice weather") is None

    def test_should_suggest_enrollment(self):
        user_info = {"full_name": "John", "phone": "+998901234567", "english_level": "B1"}
        assert IntentDetector.should_suggest_enrollment("Yes, I'm interested", user_info) is True
        assert IntentDetector.should_suggest_enrollment("No thanks", user_info) is False
        assert IntentDetector.should_suggest_enrollment("Yes", {"full_name": "John"}) is False
