
from sqlalchemy import Integer, ForeignKey, BOOLEAN
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


class EventSettings(BaseModel):
    __tablename__ = 'EventSettings'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id'), nullable=False
    )
    is_gathering: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    is_dropped: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
    is_announced: Mapped[bool] = mapped_column(
        BOOLEAN, nullable=False, default=False
    )
