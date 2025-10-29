from typing import Generic, Protocol, Self, overload, TypeVar
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.auth.interface import IUserRepository

T = TypeVar("T")


class IRepository(Protocol):
    @overload
    async def add(self, entity: dict) -> int:
        pass

    @overload
    async def get(self, _id: int) -> dict:
        pass

    @overload
    async def update(self, entity: dict) -> None:
        pass

    @overload
    async def delete(self, _id: int) -> None:
        pass

    @overload
    async def add(self, *entity: dict) -> list[int]:
        pass

    @overload
    async def get(self, *_id: int) -> list[dict]:
        pass

    @overload
    async def update(self, *entity: dict) -> None:
        pass

    @overload
    async def delete(self, *_id: int) -> None:
        pass


class IUnitOfWork(Protocol):

    users: "IUserRepository"

    async def __aenter__(self) -> "IUnitOfWork":
        pass

    async def __aexit__(self, *args):
        pass

    async def commit(self):
        pass

    async def rollback(self):
        pass
