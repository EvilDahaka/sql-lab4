from typing import Annotated
from fastapi import Depends
from src.unit_of_work import IUnitOfWork, UnitOfWork
from .service import EventService 


def get_event_service(uow: IUnitOfWork = Depends(UnitOfWork)) -> EventService:
    return EventService(uow)


EventServiceDep = Annotated[EventService, Depends(get_event_service)]