from auth.repository import UserRepositoryORM
from interface import IUnitOfWork
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from database import new_async_session


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory):
        self.session_factory: async_sessionmaker = session_factory
        self.users: UserRepositoryORM | None = None

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.users = UserRepositoryORM(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()


def get_unit_of_work():
    return SqlAlchemyUnitOfWork(new_async_session)
