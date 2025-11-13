from typing import List
from fastapi import APIRouter, status, Depends, HTTPException
from .schemas import EventCreate, EventResponse, EventUpdate
from .service import EventService 
from .exceptions import EventNotFoundError, EventPermissionError 
from .dependencies import EventServiceDep 
from src.auth.dependencies import get_current_user 
#from src.auth.schemas import UserResponce as CurrentUser 
from src.auth.schemas import UserResponce


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

@router.post(
    "/",
    response_model=EventResponse,
    status_code=status.HTTP_201_CREATED,
    summary= "Create event (потрібна авторизація)",
)
async def create_event(
    event_data: EventCreate,
    # ВИПРАВЛЕНО: Видалено '= Depends()'
    event_service: EventServiceDep, 
    current_user: UserResponce = Depends(get_current_user)):

    # ВИПРАВЛЕНО: Змінено метод з 'create' на 'create_event' (як у service.py)
    new_event = await event_service.create_event(event_data, current_user.id)
    return new_event

@router.get(
    "/{event_id}",
    response_model=EventResponse,
    summary= "Get event by id (потрібна авторизація)",
)
async def get_event(
    event_id: int,
    # ВИПРАВЛЕНО: Видалено '= Depends()'
    service: EventServiceDep,
):
    try:
        return await service.get_event(event_id)
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    

@router.get(
    "/",
    response_model=List[EventResponse],
    summary="Отримати список усіх подій",
)
async def get_all_events(
    # ВИПРАВЛЕНО: Видалено '= Depends()'
    service: EventServiceDep,
):
    """Повертає список усіх подій, доступних у системі."""
    return await service.get_all_events()


@router.patch(
    "/{event_id}",
    response_model=EventResponse,
    summary="Оновити дані події (потрібна авторизація та права власника)",
)
async def update_event(
    event_id: int,
    update_data: EventUpdate,
    # ВИПРАВЛЕНО: Видалено '= Depends()'
    service: EventServiceDep,
    current_user: UserResponce = Depends(get_current_user),
):
    """
    Оновлює подію. Дозволено лише власнику події.
    """
    try:
        return await service.update_event(
            event_id=event_id,
            update_data=update_data,
            current_user_id=current_user.id
        )
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except EventPermissionError as e:
        # Виняток, якщо користувач не є власником (403 Forbidden)
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

@router.delete(
    "/{event_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Видалити подію (потрібна авторизація та права власника)",
)
async def delete_event(
    event_id: int,
    # ВИПРАВЛЕНО: Видалено '= Depends()'
    service: EventServiceDep,
    current_user: UserResponce = Depends(get_current_user),
):
    """
    Видаляє подію. Дозволено лише власнику події.
    """
    try:
        await service.delete_event(
            event_id=event_id,
            current_user_id=current_user.id
        )
    except EventNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e),
        )
    except EventPermissionError as e:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(e),
        )

    # При успішному видаленні повертаємо 204 No Content
    return