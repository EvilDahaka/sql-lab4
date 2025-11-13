
from typing import Generic, Protocol, TypeVar

from src.interface import IRepository
from src.users.models import UserORM

T =TypeVar("T")

class IUser(Protocol):
    id:int
    username:str
    password:str
    email:str
    is_active:bool
    is_admin:bool
    

class IUserRepository(IRepository[IUser]):
    pass