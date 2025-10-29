from database import get_session
from auth.models import UserORM
from auth.schemas import TokenSchemas, UserLogin, UserRegister, UserResponce
from interface import IUnitOfWork
from auth.auth import JWTAuthCodec, get_jwt_codec
from unit_of_work import get_unit_of_work


class UserService:
    model = UserORM

    def __init__(self, uow: IUnitOfWork, codec: JWTAuthCodec):
        self.uow = uow
        self.codec = codec

    async def login(self, user_login: UserLogin):
        async with self.uow as work:

            # TODO хешування пароля
            hashed_password = user_login.password

            user = await work.users.find_email(user_login.email)

            if not user or user.password != hashed_password:
                return

            return self.__genarate_token(user.id)

    async def register(self, user: UserRegister):
        async with self.uow as work:
            # TODO хешування пароля
            hashed_password = user.password
            user.password = hashed_password
            try:
                new_user_id = await work.users.add(user.model_dump())
                await work.commit()
                return self.__genarate_token(new_user_id)
            except ValueError:
                await work.rollback()
                raise ValueError("User with this email already exists.")
                

    async def get(self, user_id: int):
        async with self.uow as work:
            user = await work.users.get(user_id)
            if not user:
                return
            return self.__user_responce(user)

    async def delele(self, user_id: int):
        async with self.uow as work:
            await work.users.delete(user_id)

    def __genarate_token(self, _id: int):
        token = self.codec.encode({"uid": _id})
        return TokenSchemas(token=token)

    def __user_responce(self, new_user: dict):
        return UserResponce(
            id=new_user.id,
            nickname=new_user.nickname,
            email=new_user.email,
            image=new_user.image_url,
        )


def get_user_servise():
    return UserService(get_unit_of_work(), get_jwt_codec())
