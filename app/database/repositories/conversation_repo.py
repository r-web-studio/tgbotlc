from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models.conversation import Conversation
from datetime import datetime


class ConversationRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_message(self, user_id: int, role: str, content: str, language: str = None, tokens_used: int = None) -> Conversation:
        msg = Conversation(user_id=user_id, role=role, content=content, language=language, tokens_used=tokens_used)
        self.session.add(msg)
        await self.session.commit()
        await self.session.refresh(msg)
        return msg

    async def get_history(self, user_id: int, limit: int = 20) -> list[Conversation]:
        result = await self.session.execute(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc()).limit(limit))
        return list(reversed(result.scalars().all()))

    async def get_full_history(self, user_id: int) -> list[Conversation]:
        result = await self.session.execute(select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.asc()))
        return list(result.scalars().all())

    async def get_message_count(self, user_id: int) -> int:
        result = await self.session.execute(select(func.count(Conversation.id)).where(Conversation.user_id == user_id))
        return result.scalar()

    async def get_recent_for_summary(self, user_id: int, since: datetime = None) -> list[Conversation]:
        query = select(Conversation).where(Conversation.user_id == user_id)
        if since:
            query = query.where(Conversation.created_at > since)
        query = query.order_by(Conversation.created_at.asc())
        result = await self.session.execute(query)
        return list(result.scalars().all())

    async def clear_history(self, user_id: int) -> int:
        result = await self.session.execute(select(Conversation).where(Conversation.user_id == user_id))
        messages = result.scalars().all()
        count = len(messages)
        for msg in messages:
            await self.session.delete(msg)
        await self.session.commit()
        return count
