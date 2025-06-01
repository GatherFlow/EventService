
from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, String
from sqlalchemy.orm import mapped_column, Mapped

from app.enum import EventFormat
from . import BaseModel


class Event(BaseModel):
    __tablename__ = 'Event'

    title: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
    duration: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    format: Mapped[EventFormat] = mapped_column(
        Enum(EventFormat), nullable=False
    )
    meeting_link: Mapped[EventFormat] = mapped_column(
        String(1000), nullable=True, default=None
    )
    location: Mapped[str] = mapped_column(
        String(500), nullable=True, default=None
    )
    announced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
