
from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


class EventTicket(BaseModel):
    __tablename__ = 'EventTicket'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id', ondelete="CASCADE"), nullable=False
    )
    title: Mapped[str] = mapped_column(
        String(100), nullable=False
    )
    description: Mapped[str] = mapped_column(
        String(255), nullable=False
    )
    price: Mapped[float] = mapped_column(
        Float, nullable=False
    )
    amount: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
    stock: Mapped[int] = mapped_column(
        Integer, nullable=False
    )
