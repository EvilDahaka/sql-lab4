from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, FileUrl
from src.users.schemas import User

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


class UserRegister(User, UserLogin):
    pass


class UserResponce(User):
    id: int = Field(ge=0)
    email: EmailStr


class TokenSchemas(BaseModel):
    token: str
    type_token: str = Field(default="Bearer")

class TokenCreate(BaseModel):
    sub:int
    username:str
    email:EmailStr
    is_admin:bool= Field(default=False)
    
class TokenInfo(TokenCreate):
    iat:datetime
    exp:datetime
    
class LoginResponce(BaseModel):
    access_token:TokenSchemas
    refresh_token:TokenSchemas