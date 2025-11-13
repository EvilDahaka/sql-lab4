from src.auth.models import RefreshTokenORM
from src.repository import RepositoryORM
from src.users.repository import UserRepository


class RefreshTokenRepository(RepositoryORM[RefreshTokenORM]):
    pass

