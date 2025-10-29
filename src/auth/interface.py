from interface import IRepository


class IUserRepository(IRepository):
    async def find_email(self, email: str):
        pass
