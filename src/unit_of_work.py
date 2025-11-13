from src.interface import IUnitOfWork
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from src.database import new_async_session
from src.repository import RepositoryORM


class SqlAlchemyUnitOfWork(IUnitOfWork):
    def __init__(self, session_factory: async_sessionmaker):
        self.session_factory = session_factory

    async def __aenter__(self):
        self.session: AsyncSession = self.session_factory()
        self.__load_repository()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
        
    def __load_repository(self):
        for field,type_ in self.__annotations__.items():
            if issubclass(type_,RepositoryORM):
                setattr(self,field,type_(self.session))
         


def get_unit_of_work():
    return SqlAlchemyUnitOfWork(new_async_session)
