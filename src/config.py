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
    private_key_path: Path = "certs/jwt-private.pem"
    public_key_path: Path = "certs/jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15
    # access_token_expire_minutes: int = 3


class S3Settings(BaseModel):
    assecc_key: str = os.getenv("S3_LOGIN")
    secret_key: str = os.getenv("S3_PASSWORD")
    endpoint: str = os.getenv("S3_ENDPOINT")
    bucket: str = os.getenv("S3_BUCKET")


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"

    db: DbSettings = DbSettings()

    auth_jwt: AuthJWT = AuthJWT()

    s3: S3Settings = S3Settings()


settings = Settings()
