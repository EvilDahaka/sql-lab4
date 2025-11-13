from src.filter import eq
import pytest
from src.interface import IRepository
from src.users.models import UserORM
from src.repository import RepositoryORM
from src.unit_of_work import get_unit_of_work
from src.seed_database import main as drop_table


@pytest.mark.asyncio
async def test_repository():
    uow = get_unit_of_work()
    async with uow as work:  # отримуємо AsyncSession з unit_of_work
        repo: IRepository[UserORM] = RepositoryORM(work.session, UserORM)
        await drop_table()

        # Додаємо запис
        data = {"username": "test", "password": "12345678", "email": "test@test.com"}
        instance = await repo.add(data)
        assert instance.username == "test"

        # Знаходимо запис
        found = await repo.find(username=eq("test"))
        assert found.id == instance.id

        # Оновлюємо запис
        updated = await repo.update(_id=instance.id, data={"username": "updated"})
        assert updated.username == "updated"

        # Видаляємо запис
        deleted = await repo.delete(_id=instance.id)
        assert deleted.id == instance.id

        # Перевіряємо find_all
        all_items = await repo.find_all(limit=10)
        assert len(all_items) == 0  # після видалення
