
from datetime import datetime
from sqlalchemy import Integer, Enum, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship, mapped_column, Mapped

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
    starting_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )
    announced_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )

    tags: Mapped[list["Tag"]] = relationship(
        "Tag",
        secondary="EventTag",
        back_populates="events"
    )


class EventTag(BaseModel):
    __tablename__ = 'EventTag'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id'), nullable=False
    )
    tag_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Tag.id'), nullable=False
    )


class Tag(BaseModel):
    __tablename__ = 'Tag'

    name: Mapped[str] = mapped_column(
        String(100), nullable=False
    )

    events: Mapped[list["Event"]] = relationship(
        "Event",
        secondary="EventTag",
        back_populates="tags"
    )
