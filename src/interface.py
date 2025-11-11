from typing import Any, Generic, Protocol, TypeVar, Sequence, overload
from pydantic import BaseModel

from src.filter import Filter, Op

T = TypeVar("T", bound=BaseModel)


class IRepository(Generic[T], Protocol):
    model: type[T]

    async def add(self, data) -> T: ...

    async def find(self, filter: Filter = Filter(), **filters: Op) -> T | None: ...

    async def find_all(
        self, offset: int = 0, limit: int = 10, filter: Filter = Filter(), **filters: Op
    ) -> list[T]: ...

    async def update(self, _id: int, data) -> T: ...

    async def delete(self, _id: int) -> T | None: ...


class IUnitOfWork(Protocol):
    async def __aenter__(self) -> "IUnitOfWork": ...
    async def __aexit__(self, *args) -> None: ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
