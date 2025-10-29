from pydantic import BaseModel, EmailStr, Field, FileUrl


class User(BaseModel):
    nickname: str = Field(min_length=3, max_length=20)


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8, max_length=32)


class UserRegister(User, UserLogin):
    pass


class UserResponce(User):
    id: int = Field(ge=0)
    email: EmailStr
    image: FileUrl | None


class TokenSchemas(BaseModel):
    token: str
    type_token: str = Field(default="Bearer")
