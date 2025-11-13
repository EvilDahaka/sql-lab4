from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import get_base_class
Base = get_base_class()
from typing import TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from src.auth.models import UserORM 

class EventORM(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE")) 
    title: Mapped[str]
    description: Mapped[str | None]
    location: Mapped[str]
    date_time: Mapped[datetime]

    
    owner: Mapped["UserORM"] = relationship(back_populates="events")
    # owner: Mapped["UserORM"] = relationship()

   