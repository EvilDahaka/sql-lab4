from typing import Annotated
from fastapi import Depends
from src.unit_of_work import get_unit_of_work 
from .service import EventService 

def get_event_service(uow = Depends(get_unit_of_work)) -> EventService:
    """
    Залежність, яка надає екземпляр EventService. 
    Вона отримує Unit of Work через функцію get_unit_of_work.
    """
    return EventService(uow)

EventServiceDep = Annotated[EventService, Depends(get_event_service)]