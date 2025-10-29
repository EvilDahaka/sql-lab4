from datetime import datetime, timedelta
from typing import Any
import jwt
from config import settings


class JWTAuthCodec:
    def __init__(self, public_key, private_key, algorithm: str, expire_minutes: int):
        self.__public_key = public_key
        self.__private_key = private_key
        self.__algorithm = algorithm
        self.__expire_minutes = expire_minutes

    def decode(self, token: str | bytes):
        return jwt.decode(
            token,
            self.__public_key,
            algorithms=self.__algorithm,
        )

    def encode(
        self,
        payload: dict[str, Any],
        expire_minutes: int | None = None,
    ):
        to_encodes = payload.copy()
        now = datetime.utcnow()
        if expire_minutes:
            expire = now + timedelta(minutes=expire_minutes)
        else:
            expire = now + timedelta(minutes=self.__expire_minutes)

        to_encodes.update(
            exp=expire,
            iat=now,
        )

        return jwt.encode(to_encodes, self.__private_key, self.__algorithm)


def get_jwt_codec():
    s = settings.auth_jwt

    with open(s.public_key_path, "r") as pub_f:
        public_key = pub_f.read()

    with open(s.private_key_path, "r") as priv_f:
        private_key = priv_f.read()

    return JWTAuthCodec(
        public_key=public_key,
        private_key=private_key,
        algorithm=s.algorithm,
        expire_minutes=s.access_token_expire_minutes,
    )
