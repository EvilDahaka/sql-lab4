from pydantic import BaseModel, EmailStr, Field, FileUrl


class User(BaseModel):
    username: str = Field(min_length=3, max_length=20)


class UserResponce(User):
    id: int = Field(ge=0)
    email: EmailStr
    image: FileUrl | None
