
from sqlalchemy import Integer, ForeignKey, Enum, JSON
from sqlalchemy.orm import mapped_column, Mapped

from app.enum import RestrictionAction

from . import BaseModel


class EventRestriction(BaseModel):
    __tablename__ = 'EventRestriction'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id'), nullable=False
    )
    action: Mapped[RestrictionAction] = mapped_column(
        Enum(RestrictionAction), nullable=False
    )
    value: Mapped[JSON] = mapped_column(
        JSON, nullable=False
    )
