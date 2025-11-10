from datetime import datetime, timezone
from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, func
from sqlalchemy.sql.sqltypes import DateTime, String, Text
from typing import TYPE_CHECKING
from src.mixin_models import CreatedAtMixin

if TYPE_CHECKING:
    from src.auth.models import UserORM


class EventORM(Base, CreatedAtMixin):
    __tablename__ = "events"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(150))
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    location: Mapped[str] = mapped_column(String(255))
    start_time: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    end_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    owner_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    owner: Mapped["UserORM"] = relationship(back_populates="events")
