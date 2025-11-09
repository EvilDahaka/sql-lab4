from src.auth.exceptions import UserRegistrationError
from src.database import get_session
from src.auth.models import UserORM
from src.auth.schemas import TokenSchemas, UserLogin, UserRegister, UserResponce
from src.exceptions import IntegrityRepositoryError
from src.filter import eq
from src.interface import IUnitOfWork
from src.auth.auth import JWTAuthCodec, get_jwt_codec
from src.unit_of_work import get_unit_of_work


class UserService:
    model = UserORM

    def __init__(self, uow: IUnitOfWork, codec: JWTAuthCodec):
        self.uow = uow
        self.codec = codec

    async def login(self, user_login: UserLogin):
        async with self.uow as work:

            # TODO хешування пароля
            hashed_password = user_login.password
            user = await work.rf(UserORM).find(email=eq(user_login.email))
            if not user or user.password != hashed_password:
                return

            return self.__genarate_token(user.id)

    async def register(self, user: UserRegister):
        async with self.uow as work:
            # TODO хешування пароля
            hashed_password = user.password
            user.password = hashed_password
            try:
                user = await work.rf(UserORM).add(entity=user.model_dump())
                await work.commit()
                return self.__genarate_token(user.id)
            except IntegrityRepositoryError:
                await work.rollback()
                raise UserRegistrationError("It email is register")

    async def get(self, user_id: int):
        async with self.uow as work:

            user = await work.rf(UserORM).find(id=eq(user_id))
            if not user:
                return
            return self.__user_responce(user)

    async def delele(self, user_id: int):
        async with self.uow as work:
            await work.rf(UserORM).delete(id=eq(user_id))

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
