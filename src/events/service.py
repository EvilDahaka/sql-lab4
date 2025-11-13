from typing import List
from src.interface import IUnitOfWork 
from src.filter import eq 
from .schemas import EventCreate, EventUpdate, EventResponse 
from .models import EventORM
from .exceptions import EventNotFoundError, EventPermissionError 


class EventService:
    """Клас сервісу для управління бізнес-логікою подій."""

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def create_event(self, event_data: EventCreate, owner_id: int) -> EventResponse:
        """Створює нову подію та призначає її поточному користувачу."""
        
        async with self.uow as work:
            event_dict = event_data.model_dump()
            
            new_event_orm = await work.rf(EventORM).add(
                entity={**event_dict, "owner_id": owner_id}
            )
            
            await work.commit() 
            
            return EventResponse.model_validate(new_event_orm) 

    
    
    async def get_event(self, event_id: int) -> EventResponse:
        """Повертає одну подію за її ID."""
        
        async with self.uow as work:
            event_orm = await work.rf(EventORM).find_one(id=eq(event_id))
            
            if not event_orm:
                raise EventNotFoundError(f"Подію з ID {event_id} не знайдено.")
                
            return EventResponse.model_validate(event_orm)
            
    async def get_all_events(self) -> List[EventResponse]:
        """Повертає список усіх подій."""
        
        async with self.uow as work:
            events_orm = await work.rf(EventORM).find_all()
            
            return [EventResponse.model_validate(e) for e in events_orm]

    

    async def update_event(self, event_id: int, update_data: EventUpdate, current_user_id: int) -> EventResponse:
        """Оновлює дані події після перевірки прав доступу."""
        
        async with self.uow as work:
            event_orm = await work.rf(EventORM).find_one(id=eq(event_id))
            
            if not event_orm:
                raise EventNotFoundError(f"Подію з ID {event_id} не знайдено.")

            # БІЗНЕС-ПРАВИЛО: Перевірка прав
            if event_orm.owner_id != current_user_id:
                raise EventPermissionError("Ви можете оновлювати лише власні події.")
            
            update_dict = update_data.model_dump(exclude_unset=True) 
            
            updated_event_orm = await work.rf(EventORM).update(
                filters={"id": eq(event_id)},
                values=update_dict
            )

            await work.commit()
            
            if updated_event_orm is None:
                raise EventNotFoundError(f"Подію з ID {event_id} не знайдено.")
            
            return EventResponse.model_validate(updated_event_orm)

    

    async def delete_event(self, event_id: int, current_user_id: int) -> bool:
        """Видаляє подію після перевірки прав доступу."""
        
        async with self.uow as work:
            event_orm = await work.rf(EventORM).find_one(id=eq(event_id))
            
            if not event_orm:
                raise EventNotFoundError(f"Подію з ID {event_id} не знайдено.")

            # БІЗНЕС-ПРАВИЛО: Перевірка прав
            if event_orm.owner_id != current_user_id:
                raise EventPermissionError("Ви можете видаляти лише власні події.")
            
            rows_deleted = await work.rf(EventORM).delete(id=eq(event_id))
            
            await work.commit()

            return rows_deleted > 0