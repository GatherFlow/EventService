
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


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
