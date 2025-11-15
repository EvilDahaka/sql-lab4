from pydantic import BaseModel
from datetime import datetime

class TicketBase(BaseModel):
    event_id: int
    ticket_type: str = "Standart"
    price: int


class Config:
    from_attributes = True

class TicketCreate(TicketBase):
    pass
class TicketResponse(TicketBase):
    id: int
    owner_id: int
    is_used: bool
    created_at: datetime