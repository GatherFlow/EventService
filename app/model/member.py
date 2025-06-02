
from sqlalchemy import Integer, ForeignKey, Enum, String
from sqlalchemy.orm import mapped_column, Mapped

from app.enum import MemberRole

from . import BaseModel


class Member(BaseModel):
    __tablename__ = 'Member'

    event_id: Mapped[int] = mapped_column(
        Integer, ForeignKey('Event.id', ondelete="CASCADE"), nullable=False
    )
    user_id: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    role: Mapped[MemberRole] = mapped_column(
        Enum(MemberRole), nullable=False
    )
