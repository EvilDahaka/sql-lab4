from typing import Any, Generic, Protocol, TypeVar, Sequence, overload
from pydantic import BaseModel

from src.filter import Op

T = TypeVar("T", bound=BaseModel)


class IRepository(Protocol[T]):

    model: type[T]

    def __call__(self, model: type) -> "IRepository":
        """Створює конкретний репозиторій для моделі."""
        ...

    @overload
    async def add(self, entity: dict) -> T: ...
    @overload
    async def add(self, *entities: dict) -> Sequence[T]: ...

    @overload
    async def find(self, limit: int, offset: int, **filters: Any) -> Sequence[T]: ...
    @overload
    async def find(self, **filters: Any) -> T | None: ...

    @overload
    async def update(self, *entities: dict, **filters) -> Sequence[T]: ...

    @overload
    async def delete(self, **filter) -> Sequence[T]: ...


class IUnitOfWork(Protocol):

    rf: IRepository[Any]

    async def __aenter__(self) -> "IUnitOfWork": ...
    async def __aexit__(self, *args) -> None: ...

    async def commit(self) -> None: ...
    async def rollback(self) -> None: ...
