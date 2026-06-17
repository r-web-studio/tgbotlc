from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models.memory import Memory
from datetime import datetime
from typing import Optional


class MemoryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_user_and_key(self, user_id: int, key: str) -> Optional[Memory]:
        result = await self.session.execute(select(Memory).where(Memory.user_id == user_id, Memory.key == key))
        return result.scalar_one_or_none()

    async def get_by_user(self, user_id: int) -> list[Memory]:
        result = await self.session.execute(select(Memory).where(Memory.user_id == user_id))
        return list(result.scalars().all())

    async def upsert(self, user_id: int, key: str, value: str, category: str = "info") -> Memory:
        existing = await self.get_by_user_and_key(user_id, key)
        if existing:
            existing.value = value
            existing.updated_at = datetime.utcnow()
            await self.session.commit()
            await self.session.refresh(existing)
            return existing
        memory = Memory(user_id=user_id, key=key, value=value, category=category)
        self.session.add(memory)
        await self.session.commit()
        await self.session.refresh(memory)
        return memory

    async def get_all_by_user_as_dict(self, user_id: int) -> dict[str, str]:
        memories = await self.get_by_user(user_id)
        return {m.key: m.value for m in memories}

    async def delete(self, user_id: int, key: str) -> bool:
        memory = await self.get_by_user_and_key(user_id, key)
        if memory:
            await self.session.delete(memory)
            await self.session.commit()
            return True
        return False
