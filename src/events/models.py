from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import get_base_class
from src.mixin_models import CreatedAtMixin

Base = get_base_class()
from typing import TYPE_CHECKING
from datetime import datetime


if TYPE_CHECKING:
    from src.users.models import UserORM
    from src.tickets.models import TicketsORM


class EventORM(Base, CreatedAtMixin):
    __tablename__ = "events"
    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str]
    description: Mapped[str | None]
    location: Mapped[str]
    date_time: Mapped[datetime]

    owner: Mapped["UserORM"] = relationship(back_populates="events")
    tickets: Mapped[list["TicketsORM"]] = relationship(
        "TicketsORM",
        back_populates="event",
        cascade="all, delete-orphan",  # Optional: add cascade for ticket cleanup
    )
    # owner: Mapped["UserORM"] = relationship()
