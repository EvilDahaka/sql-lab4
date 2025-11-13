from src.auth.models import RefreshTokenORM
from src.repository import RepositoryORM
from src.unit_of_work import SqlAlchemyUnitOfWork
from src.users.repository import UserRepository


class RefreshTokenRepository(RepositoryORM[RefreshTokenORM]):
    pass


class AuthUnitOfWork(SqlAlchemyUnitOfWork):
    refresh_token: RefreshTokenRepository
    user: UserRepository
