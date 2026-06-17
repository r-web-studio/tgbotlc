from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models.follow_up import FollowUp
from datetime import datetime


class FollowUpRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, message: str, scheduled_at: datetime) -> FollowUp:
        fu = FollowUp(user_id=user_id, message=message, scheduled_at=scheduled_at)
        self.session.add(fu)
        await self.session.commit()
        await self.session.refresh(fu)
        return fu

    async def get_pending(self) -> list[FollowUp]:
        now = datetime.utcnow()
        result = await self.session.execute(select(FollowUp).where(FollowUp.status == "pending", FollowUp.scheduled_at <= now))
        return list(result.scalars().all())

    async def mark_sent(self, follow_up: FollowUp) -> FollowUp:
        follow_up.status = "sent"
        follow_up.sent_at = datetime.utcnow()
        await self.session.commit()
        return follow_up

    async def mark_failed(self, follow_up: FollowUp) -> FollowUp:
        follow_up.status = "failed"
        await self.session.commit()
        return follow_up

    async def has_pending_for_user(self, user_id: int) -> bool:
        result = await self.session.execute(select(func.count(FollowUp.id)).where(FollowUp.user_id == user_id, FollowUp.status == "pending"))
        return result.scalar() > 0
