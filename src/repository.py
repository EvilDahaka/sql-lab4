from typing import Any, Callable, TypeVar
from sqlalchemy import Result, Select, Tuple, delete, insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import StatementError, IntegrityError, SQLAlchemyError

from src.database import Base
from src.exceptions import IntegrityRepositoryError, InvalidQueryError, RepositoryError
from src.filter import Filter, FilterHeadler, Op
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
            return [
                func(arg, **kwargs) for arg in args
            ]  # декілька аргументів → передаємо список

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
M = TypeVar("M", bound=Base)


@repository
class RepositoryORM(IRepository):

    def __init__(self, session: AsyncSession, model: T):
        self.session = session
        self.model = model
        self._filter = FilterHeadler(self.model)

    @execute
    async def find_all(
        self, joins=None, limit=10, offset=0, _filter: Filter = Filter(), **filters
    ):
        stmt = await self.__find(joins=joins, _filter=_filter, filters=filters)
        stmt = stmt.offset(offset).limit(limit)
        res = await self.session.execute(stmt)
        return res.scalars().all()

    @execute
    async def find(self, joins=None, _filter: Filter = Filter(), **filters):
        stmt = await self.__find(joins=joins, _filter=_filter, filters=filters)
        res = await self.session.execute(stmt)
        return res.scalar_one_or_none()

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

    async def __find(
        self, joins: set[type[M]], _filter: Filter, filters: dict[str, Any]
    ) -> Select[Tuple]:
        stmt = select(self.model)
        if joins:
            for j in joins:
                stmt = stmt.join(j)
        f = self._resolve_filter(_filter, filters)
        stmt = stmt.where(*f)
        return stmt

    def _resolve_filter(self, _filter: Filter, _filters: dict) -> list[Callable]:
        if not isinstance(_filter, Filter):
            raise TypeError(f"_filter must be Filter, not {type(_filter)}")
        _filter.overload(**_filters)
        return self._filter.to_conditions(_filter)
