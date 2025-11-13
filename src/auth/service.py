from src.auth.exceptions import InvalidRefreshToken, LoginError, RegistrationError
from src.auth.interface import IRefreshTokenRepository
from src.auth.models import RefreshTokenORM
from src.auth.repository import AuthUnitOfWork
from src.database import get_session
from src.users.interface import IUser, IUserRepository
from src.users.models import UserORM
from src.auth.schemas import LoginResponce, TokenCreate, TokenSchemas, UserLogin, UserRegister, UserResponce
from src.exceptions import IntegrityRepositoryError, RepositoryError
from src.filter import eq
from src.interface import IUnitOfWork
from src.auth.jwt_codec import JWTAuthCodec, get_jwt_codec
from src.unit_of_work import get_unit_of_work
from typing import Type

from src.users.repository import UserRepository


class AuthService:

    def __init__(
        self,
        uow: IUnitOfWork,
        codec: JWTAuthCodec,
    ):
        self.uow = uow
        self.codec = codec

    async def login(self, user_login: UserLogin):
        async with self.uow as work:
            # TODO хешування пароля
            hashed_password = user_login.password
            user = await work.users.find(email=eq(user_login.email))
            if not user or user.password != hashed_password:
                raise LoginError("Uncorrect password")
            return self.__genarate_tokens(user,work)

    async def register(self, user_data: UserRegister):
        async with self.uow as work:
            # TODO хешування пароля
            hashed_password = user_data.password
            user_data.password = hashed_password
            try:
                user = await work.users.add(user_data.model_dump())
                await work.commit()
                return self.__genarate_tokens(user,work)
            except IntegrityRepositoryError:
                await work.rollback()
                raise RegistrationError("It email is register")
            
    async def refresh(self,refresh_token:str):
        async with self.uow as work:
            token_info = self.codec.decode(refresh_token)
            token = await work.refresh_tokens.find(token=eq(refresh_token))
            if token.revoked: # type: ignore
                raise InvalidRefreshToken("Token revoked")
            user = await work.users.find(id=eq(token.id)) # type: ignore
            if user.is_active: # type: ignore
                return self.__genarate_token(user)
            raise InvalidRefreshToken("User is ban")
            
    async def __genarate_tokens(self,user:IUser,work:IUnitOfWork):
        refresh_token = self.__genarate_token(user,expire_minutes=7*24*60)
        access_token = self.__genarate_token(user)
        await work.refresh_tokens.add({"token":refresh_token,"user_id":user.id})
        return LoginResponce(
            access_token=access_token,
            refresh_token=refresh_token
        )

    def __genarate_token(self, user:IUser,expire_minutes:int=15):
        payload = TokenCreate(
                    sub=user.id,
                    username=user.username,
                    email=user.email,
                    is_active=user.is_active
                )
        token = self.codec.encode(payload,expire_minutes=expire_minutes)
        return TokenSchemas(token=token)


def get_user_servise():
    return AuthService(get_unit_of_work(), get_jwt_codec())
