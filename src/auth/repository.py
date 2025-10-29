from sqlalchemy import select
from repository import RepositoryORM, execute
from auth.models import UserORM

from auth.interface import IUserRepository

class UserRepositoryORM(RepositoryORM, IUserRepository):
    model = UserORM

    @execute
    async def find_email(self, email: str):
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
