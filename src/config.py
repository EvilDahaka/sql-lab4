import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings

load_dotenv()


class DbSettings(BaseModel):
    url: str = os.getenv("DATABASE_URL")
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = Path("src/certs/jwt-private.pem")
    public_key_path: Path = Path("src/certs/jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15


class Settings(BaseSettings):
    path_root: Path = Path(__file__).parent.parent
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()
