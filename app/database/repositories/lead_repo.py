from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.database.models.user import User
from app.database.models.lead_status import LeadStatusHistory


class LeadRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_status(self, user_id: int, new_status: str, reason: str = None) -> LeadStatusHistory:
        user_result = await self.session.execute(select(User).where(User.id == user_id))
        user = user_result.scalar_one_or_none()
        old_status = user.lead_status if user else None

        if user:
            user.lead_status = new_status
            await self.session.commit()

        history = LeadStatusHistory(user_id=user_id, old_status=old_status, new_status=new_status, reason=reason)
        self.session.add(history)
        await self.session.commit()
        await self.session.refresh(history)
        return history

    async def get_history(self, user_id: int) -> list[LeadStatusHistory]:
        result = await self.session.execute(select(LeadStatusHistory).where(LeadStatusHistory.user_id == user_id).order_by(LeadStatusHistory.created_at.desc()))
        return list(result.scalars().all())
