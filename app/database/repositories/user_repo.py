from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models.user import User
from datetime import datetime, timedelta
from typing import Optional


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    async def get_by_telegram_id(self, telegram_id: int) -> Optional[User]:
        result = await self.session.execute(select(User).where(User.telegram_id == telegram_id))
        return result.scalar_one_or_none()

    async def create(self, telegram_id: int, username: str = None, first_name: str = None, last_name: str = None, language: str = "en") -> User:
        user = User(telegram_id=telegram_id, username=username, first_name=first_name, last_name=last_name, language=language)
        self.session.add(user)
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        user.updated_at = datetime.utcnow()
        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def update_last_interaction(self, user: User) -> User:
        user.last_interaction = datetime.utcnow()
        await self.session.commit()
        return user

    async def get_inactive_users(self, days: int = 3) -> list[User]:
        cutoff = datetime.utcnow() - timedelta(days=days)
        result = await self.session.execute(select(User).where(User.last_interaction < cutoff, User.is_active == True, User.is_enrolled == False))
        return list(result.scalars().all())

    async def count_all(self) -> int:
        result = await self.session.execute(select(func.count(User.id)))
        return result.scalar()

    async def count_by_lead_status(self, status: str) -> int:
        result = await self.session.execute(select(func.count(User.id)).where(User.lead_status == status))
        return result.scalar()

    async def count_enrolled(self) -> int:
        result = await self.session.execute(select(func.count(User.id)).where(User.is_enrolled == True))
        return result.scalar()

    async def search(self, query: str) -> list[User]:
        pattern = f"%{query}%"
        result = await self.session.execute(select(User).where(User.full_name.ilike(pattern) | User.username.ilike(pattern) | User.phone.ilike(pattern)).limit(50))
        return list(result.scalars().all())

    async def get_all(self, offset: int = 0, limit: int = 50) -> list[User]:
        result = await self.session.execute(select(User).order_by(User.created_at.desc()).offset(offset).limit(limit))
        return list(result.scalars().all())

    async def soft_delete(self, user: User) -> User:
        user.is_active = False
        await self.session.commit()
        return user
