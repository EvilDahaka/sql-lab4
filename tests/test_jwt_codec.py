from src.auth.auth import get_jwt_codec
from src.config import settings


def test_codec():
    codec = get_jwt_codec()
    payload = {"sub": "1234567890", "name": "John Doe", "admin": True}
    token = codec.encode(payload, expire_minutes=1)
    decoded_payload = codec.decode(token)
    assert decoded_payload["sub"] == payload["sub"]
    assert decoded_payload["name"] == payload["name"]
    assert decoded_payload["admin"] == payload["admin"]
