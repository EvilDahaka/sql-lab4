from jwt import InvalidTokenError
from src.auth.exceptions import InvalidRefreshToken, LoginError, RegistrationError
from src.users.interface import IUser
from src.auth.schemas import LoginResponce, TokenCreate, TokenSchemas, UserLogin, UserRegister
from src.exceptions import IntegrityRepositoryError
from src.filter import eq
from src.interface import IUnitOfWork
from src.auth.jwt_codec import JWTAuthCodec, get_jwt_codec
from src.unit_of_work import get_unit_of_work




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
            return await self.__genarate_tokens(user,work)

    async def register(self, user_data: UserRegister):
        async with self.uow as work:
            # TODO хешування пароля
            hashed_password = user_data.password
            user_data.password = hashed_password
            try:
                user = await work.users.add(user_data.model_dump())
                return await self.__genarate_tokens(user,work)
            except IntegrityRepositoryError:
                raise RegistrationError("It email is register")
            
    async def refresh(self,refresh_token:str):
        async with self.uow as work:
            token = await work.refresh_tokens.find(token=eq(refresh_token))
            
            if not token:
                raise InvalidRefreshToken("token invalid ")
            if token.revoked: # type: ignore
                raise InvalidRefreshToken("Token revoked")
            user = await work.users.find(id=eq(token.user_id)) 
            await work.commit()# type: ignore
            if user.is_active: # type: ignore
                self.checking_invalid_token(refresh_token)
                return self.__genarate_token(user)
            raise InvalidRefreshToken("User is ban")
        
    async def logout(self,refresh_token:str):
        self.checking_invalid_token(refresh_token)
        async with self.uow as work:
            token = await work.refresh_tokens.find(token=eq(refresh_token))
            if token:
                if token.revoked == False:
                    await work.refresh_tokens.update(token.id,{"revoked":True})
                    return
            raise InvalidRefreshToken()
                
    def checking_invalid_token(self,refresh_token):
        try:
            token_info = self.codec.decode(refresh_token)
        except InvalidTokenError:
                InvalidRefreshToken("token invalid ")
            
    async def __genarate_tokens(self,user:IUser,work:IUnitOfWork):
        refresh_token = self.__genarate_token(user,expire_minutes=7*24*60)
        access_token = self.__genarate_token(user)
        await work.refresh_tokens.add({"token":refresh_token.token,"user_id":user.id})
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
