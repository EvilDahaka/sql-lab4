from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String, Enum, Boolean
from sqlalchemy.orm import relationship
from datetime import datetime

class tickets(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index = True)
    event_id = Column(Integer, ForeignKey('events.id', ondelete="CASCADE"))
    owner_id = Column(Integer, ForeignKey('users.id', nullable=False))

    ticket_type = Column(String, default="Standart", nullable=False)
    price = Column(Integer, nullable=False)
    is_used = Column(Boolean, default=False, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    event = relationship("Event", back_populates="tickets")
    owner = relationship("User", back_populates="tickets")