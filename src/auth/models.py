from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from src.database import Base


class UserORM(Base):
    __tablename__ = "users"
    nickname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    image_url: Mapped[str] = mapped_column(nullable=True)
