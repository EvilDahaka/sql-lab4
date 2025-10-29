from typing import Callable
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import StatementError, IntegrityError

from database import Base
from interface import T, IRepository


def execute(func: Callable):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (IntegrityError, StatementError):
            raise ValueError("Data integrity error occurred during the operation.")

    return wrapper


def overload_responce(func: Callable):
    async def wrapper(*args, **kwargs):

        result = await func(*args, **kwargs)
        if len(result) == 1:
            return result[0]
        return result

    return wrapper


class RepositoryORM(IRepository):
    model: Base = None

    def __init__(self, session: AsyncSession):
        self.session = session

    @execute
    @overload_responce
    async def get(self, *_id: int) -> int | list[int]:
        res = []
        for model_id in _id:
            stmt = select(self.model).where(self.model.id == model_id)
            data = await self.session.execute(stmt)
            res.append(data.scalar_one_or_none())
        return res

    @execute
    @overload_responce
    async def add(self, *entity: dict) -> int | list[int]:
        res = []
        for data in entity:
            stmt = insert(self.model).values(**data).returning(self.model.id)
            data = await self.session.execute(stmt)
            res.append(data.scalar_one_or_none())
        return res

    @execute
    async def update(self, *entity: dict):
        for data in entity:
            stmt = update(self.model).where(self.model.id == data["id"]).values(**data)
            await self.session.execute(stmt)

    @execute
    async def delete(self, *_id: int):
        for model_id in _id:
            stmt = delete(self.model).where(self.model.id == model_id)
            model_id = await self.session.execute(stmt)
