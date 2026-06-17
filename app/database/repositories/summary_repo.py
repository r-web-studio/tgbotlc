from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models.summary import Summary
from typing import Optional


class SummaryRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, summary: str, key_points: str = None, message_count: int = 0) -> Summary:
        s = Summary(user_id=user_id, summary=summary, key_points=key_points, message_count=message_count)
        self.session.add(s)
        await self.session.commit()
        await self.session.refresh(s)
        return s

    async def get_latest(self, user_id: int) -> Optional[Summary]:
        result = await self.session.execute(select(Summary).where(Summary.user_id == user_id).order_by(Summary.created_at.desc()).limit(1))
        return result.scalar_one_or_none()

    async def get_all_for_user(self, user_id: int) -> list[Summary]:
        result = await self.session.execute(select(Summary).where(Summary.user_id == user_id).order_by(Summary.created_at.desc()))
        return list(result.scalars().all())
