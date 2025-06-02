
from sqlalchemy import Integer, ForeignKey, String, Float
from sqlalchemy.orm import mapped_column, Mapped

from . import BaseModel


class SearchQuery(BaseModel):
    __tablename__ = 'SearchQuery'

    user_id: Mapped[str] = mapped_column(
        String(200), nullable=False
    )
    value: Mapped[str] = mapped_column(
        String(500), nullable=False
    )
