from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class EventBase(BaseModel):
    title: str = Field(min_length=5, max_length=150, description="Назва події")
    description: Optional[str] = Field(None, max_length=5000, description="Детальний опис події")
    location: str = Field(min_length=5, max_length=255, description="Місце проведення події")

    start_time: datetime = Field(description="Дата і час початку події")
    end_time: Optional[datetime] = Field(None, description="Дата і час закінчення події")


class EventCreate(EventBase):
    pass

class EventUpdate(EventBase):
    title: Optional[str] = Field(None, min_length=5, max_length=150)
    description: Optional[str] = Field(None, max_length=5000)
    location: Optional[str] = Field(None, min_length=5, max_length=255)
    start_time: Optional[datetime] = Field(None)
    end_time: Optional[datetime] = Field(None)


class EventResponse(EventBase):
    id: int
    owner_id: int
    created_at: datetime

class Config:
    from_attributes = True
    