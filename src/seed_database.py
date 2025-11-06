from src.database import Base, engine
from src.auth.models import *


async def main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Базу даних і таблиці створено успішно.")


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
