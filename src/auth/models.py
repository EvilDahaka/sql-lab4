from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, ForeignKey, Integer
from src.database import Base
from src.mixin_models import CreatedAtMixin


class RefreshTokenORM(Base, CreatedAtMixin):
    __tablename__ = "refresh_token"
    token: Mapped[str]
    user_id = Column(Integer, ForeignKey("users.id"))
    revoked: Mapped[bool]

    user = relationship("UserORM", back_populates="tokens")
