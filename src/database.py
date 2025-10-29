from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from fastapi import Depends
from config import settings

engine = create_async_engine(**settings.db.dict())
new_async_session = async_sessionmaker(engine, expire_on_commit=False)


async def get_session():
    async with new_async_session() as session:
        yield session


class Base(DeclarativeBase):
    pass
