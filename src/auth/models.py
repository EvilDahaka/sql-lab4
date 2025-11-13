from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Boolean, Column, ForeignKey, Integer, text
from src.database import Base
from src.mixin_models import CreatedAtMixin


class RefreshTokenORM(Base, CreatedAtMixin):
    __tablename__ = "refresh_tokens"
    token: Mapped[str]
    user_id = Column(Integer, ForeignKey("users.id"))
    revoked: Mapped[bool] = mapped_column(Boolean, server_default=text("false"))

    user = relationship("UserORM", back_populates="tokens")
