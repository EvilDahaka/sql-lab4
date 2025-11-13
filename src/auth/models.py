from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import get_base_class
Base = get_base_class()
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from src.events.models import EventORM

class UserORM(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    image_url: Mapped[str] = mapped_column(nullable=True)

    events: Mapped[List["EventORM"]] = relationship(back_populates="owner")
    #events: Mapped[List["EventORM"]] = relationship()
