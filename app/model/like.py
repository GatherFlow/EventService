
from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


class Like(BaseModel):
    __tablename__ = 'Like'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id', ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
