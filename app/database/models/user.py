from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import BigInteger, Boolean, DateTime, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base

if TYPE_CHECKING:
    from app.database.models.conversation import Conversation
    from app.database.models.enrollment import Enrollment
    from app.database.models.memory import Memory
    from app.database.models.summary import Summary


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    first_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    last_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    full_name: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    age: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    phone: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    english_level: Mapped[Optional[str]] = mapped_column(String(20), nullable=True)
    goal: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    preferred_time: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    language: Mapped[str] = mapped_column(String(5), default="en")
    lead_status: Mapped[str] = mapped_column(String(20), default="cold")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_enrolled: Mapped[bool] = mapped_column(Boolean, default=False)
    last_interaction: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

    memories: Mapped[list[Memory]] = relationship("Memory", back_populates="user", lazy="selectin")
    conversations: Mapped[list[Conversation]] = relationship("Conversation", back_populates="user", lazy="selectin")
    enrollments: Mapped[list[Enrollment]] = relationship("Enrollment", back_populates="user", lazy="selectin")
    summaries: Mapped[list[Summary]] = relationship("Summary", back_populates="user", lazy="selectin")
