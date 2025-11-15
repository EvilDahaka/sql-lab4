from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

from src.mixin_models import CreatedAtMixin


class TicketsORM(Base, CreatedAtMixin):
    __tablename__ = "tickets"
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id", ondelete="CASCADE"))
    ticket_type: Mapped[str] = mapped_column(default="Standart")
    price: Mapped[int]
    status: Mapped[str] = mapped_column(default="reserved")
    is_used: Mapped[bool] = mapped_column(default=False)

    event = relationship("EventORM", back_populates="tickets")
    owner = relationship("UserORM", back_populates="tickets")
