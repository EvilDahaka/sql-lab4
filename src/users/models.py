from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String
from src.auth.models import RefreshTokenORM
from src.database import Base
from src.mixin_models import CreatedAtMixin


class UserORM(Base, CreatedAtMixin):
    __tablename__ = "users"
    username: Mapped[str]
    email: Mapped[str] = mapped_column(String(255), unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True)
    is_admin: Mapped[bool] = mapped_column(default=False)

    tokens: Mapped[list["RefreshTokenORM"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
