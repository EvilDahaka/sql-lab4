from typing import Callable, TypeVar
from sqlalchemy import delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import StatementError, IntegrityError, SQLAlchemyError

from src.database import Base
from src.exceptions import IntegrityRepositoryError, InvalidQueryError, RepositoryError
from src.filter import FilterHeadler, Op
from src.interface import IRepository
from typing import TypeVar, Generic


def execute(func: Callable):
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError as e:
            raise IntegrityRepositoryError("Integrity error during DB operation") from e
        except StatementError as e:
            raise InvalidQueryError("Invalid query or filter") from e
        except SQLAlchemyError as e:
            raise RepositoryError from e

    return wrapper


def overload_response(func: Callable):
    async def wrapper(*args, **kwargs):
        if len(args) == 1:
            return await func(*args, **kwargs)  # один аргумент → повертаємо одразу
        else:
            return await func(
                list(args), **kwargs
            )  # декілька аргументів → передаємо список

    return wrapper


def repository(cls):
    """
    Декоратор, який перетворює клас у 'ленивий' репозиторій.
    Екземпляр створюється тільки при виклику з моделлю.
    """

    class LazyRepo:
        def __init__(self, session: AsyncSession):
            self.session = session

        def __call__(self, model: type[Base]):
            return cls(self.session, model)  # створюємо RepositoryORM тільки тут

    return LazyRepo


T = TypeVar("T", bound=Base)


@repository
class RepositoryORM(IRepository):

    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model
        self._filter = FilterHeadler(self.model)

    @execute
    async def find(self, limit=None, offset=None, **_filter):
        stmt = select(self.model).where(*self._filter(**_filter))
        if offset is not None and limit is not None:
            stmt = stmt.offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return res.scalars().all() if limit else res.scalar_one_or_none()

    @execute
    @overload_response
    async def add(self, entity: dict):
        stmt = insert(self.model).values(**entity).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar_one()

    @execute
    async def update(self, entity: dict, **_filters):
        stmt = (
            update(self.model)
            .where(*self._filter(**_filters))
            .values(**{k: v for k, v in entity.items() if k != "id"})
            .returning(self.model)
        )
        res = await self.session.execute(stmt)
        return res.scalar().all()

    @execute
    async def delete(self, **filters):
        stmt = delete(self.model).where(*self._filter(**filters)).returning(self.model)
        res = await self.session.execute(stmt)
        return res.scalar().all()
