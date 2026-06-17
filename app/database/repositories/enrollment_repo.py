from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.database.models.enrollment import Enrollment
from typing import Optional


class EnrollmentRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user_id: int, full_name: str, age: int, phone: str, english_level: str, goal: str, preferred_time: str) -> Enrollment:
        enrollment = Enrollment(user_id=user_id, full_name=full_name, age=age, phone=phone, english_level=english_level, goal=goal, preferred_time=preferred_time)
        self.session.add(enrollment)
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment

    async def get_by_user(self, user_id: int) -> Optional[Enrollment]:
        result = await self.session.execute(select(Enrollment).where(Enrollment.user_id == user_id).order_by(Enrollment.created_at.desc()))
        return result.scalar_one_or_none()

    async def get_all(self) -> list[Enrollment]:
        result = await self.session.execute(select(Enrollment).order_by(Enrollment.created_at.desc()))
        return list(result.scalars().all())

    async def update_status(self, enrollment: Enrollment, status: str, notes: str = None) -> Enrollment:
        enrollment.status = status
        if notes:
            enrollment.notes = notes
        await self.session.commit()
        await self.session.refresh(enrollment)
        return enrollment

    async def count(self) -> int:
        result = await self.session.execute(select(func.count(Enrollment.id)))
        return result.scalar()
