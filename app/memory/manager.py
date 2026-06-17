from sqlalchemy.ext.asyncio import AsyncSession
from app.database.repositories.memory_repo import MemoryRepository
from app.database.repositories.user_repo import UserRepository
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class MemoryManager:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.memory_repo = MemoryRepository(session)
        self.user_repo = UserRepository(session)
    
    async def store(self, user_id: int, key: str, value: str, category: str = "info") -> None:
        await self.memory_repo.upsert(user_id, key, value, category)
        logger.debug(f"Stored memory for user {user_id}: {key}={value}")
    
    async def retrieve(self, user_id: int, key: str) -> Optional[str]:
        memory = await self.memory_repo.get_by_user_and_key(user_id, key)
        return memory.value if memory else None
    
    async def get_all(self, user_id: int) -> dict[str, str]:
        return await self.memory_repo.get_all_by_user_as_dict(user_id)
    
    async def delete(self, user_id: int, key: str) -> bool:
        return await self.memory_repo.delete(user_id, key)
    
    async def format_user_context(self, user_id: int) -> str:
        memories = await self.get_all(user_id)
        if not memories:
            return "No information collected yet."
        
        parts = []
        for key, value in memories.items():
            parts.append(f"- {key}: {value}")
        return "\n".join(parts)
    
    async def extract_and_store_from_message(self, user_id: int, text: str) -> list[str]:
        stored = []
        text_lower = text.lower()
        
        # Name detection
        name_patterns = ["my name is", "i'm called", "call me", "меня зовут", "мени исмим", "meni ismim"]
        for pattern in name_patterns:
            if pattern in text_lower:
                idx = text_lower.index(pattern) + len(pattern)
                name = text[idx:].strip().split("\n")[0].split(".")[0].split(",")[0].strip()
                if name and 2 < len(name) < 100 and not any(c.isdigit() for c in name):
                    await self.store(user_id, "full_name", name, "info")
                    stored.append("full_name")
                    break
        
        # Phone detection
        import re
        phone_match = re.search(r'[\+]?[\d\s\-\(\)]{10,18}', text)
        if phone_match:
            phone = phone_match.group().strip()
            if len(re.sub(r'\D', '', phone)) >= 10:
                await self.store(user_id, "phone", phone, "info")
                stored.append("phone")
        
        # Level detection
        level_map = {"a1": "A1", "a2": "A2", "b1": "B1", "b2": "B2", "c1": "C1", "c2": "C2",
                      "beginner": "A1", "elementary": "A2", "intermediate": "B1", 
                      "upper intermediate": "B2", "advanced": "C1"}
        for key, value in level_map.items():
            if key in text_lower:
                await self.store(user_id, "english_level", value, "info")
                stored.append("english_level")
                break
        
        # Age detection
        age_match = re.search(r'\b(\d{1,2})\b\s*(years?\s*old|лет|yosh)', text_lower)
        if age_match:
            age = int(age_match.group(1))
            if 10 <= age <= 80:
                await self.store(user_id, "age", str(age), "info")
                stored.append("age")
        
        # Goal detection
        goal_keywords = {
            "ielts": "IELTS", "toefl": "TOEFL", "business": "Business English",
            "travel": "Travel", "work": "Work", "study": "Study Abroad",
            "general": "General English", "kids": "Kids English"
        }
        for keyword, goal in goal_keywords.items():
            if keyword in text_lower:
                await self.store(user_id, "goal", goal, "preference")
                stored.append("goal")
                break
        
        return stored
