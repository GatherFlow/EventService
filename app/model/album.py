
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


class EventAlbum(BaseModel):
    __tablename__ = 'EventAlbum'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id', ondelete="CASCADE"), nullable=False
    )
    img: Mapped[str] = mapped_column(
        String(1000), nullable=False
    )
