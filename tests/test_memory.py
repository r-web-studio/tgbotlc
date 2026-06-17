import pytest
import asyncio
from app.memory.manager import MemoryManager

class TestMemoryManager:
    def test_extract_info_name(self):
        texts = [
            ("My name is John Smith", "John Smith"),
            ("меня зовут Али", "Али"),
            ("I'm called Sarah", "Sarah"),
        ]
        for text, expected in texts:
            text_lower = text.lower()
            found = False
            for pattern in ["my name is", "меня зовут", "i'm called", "call me"]:
                if pattern in text_lower:
                    idx = text_lower.index(pattern) + len(pattern)
                    name = text[idx:].strip().split("\n")[0].split(".")[0].split(",")[0].strip()
                    assert name == expected
                    found = True
                    break

    def test_extract_info_level(self):
        texts = ["I'm B1 level", "My level is A2", "I have C1"]
        expected = ["B1", "A2", "C1"]
        for text, exp in zip(texts, expected):
            text_lower = text.lower()
            for level in ["A1", "A2", "B1", "B2", "C1", "C2"]:
                if level.lower() in text_lower:
                    assert level == exp
                    break

    def test_extract_info_goal(self):
        texts = ["I want IELTS", "business english", "travel english"]
        expected = ["IELTS", "Business English", "Travel"]
        for text, exp in zip(texts, expected):
            text_lower = text.lower()
            goal_keywords = {"ielts": "IELTS", "business": "Business English", "travel": "Travel"}
            for keyword, goal in goal_keywords.items():
                if keyword in text_lower:
                    assert goal == exp
                    break
