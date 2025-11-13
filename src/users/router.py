from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Annotated
# from src.auth.dependencies import AuthUserDep

router = APIRouter(prefix="/users")

http_bearer = HTTPBearer()

users = {"1": "admin"}


def get(creds: HTTPAuthorizationCredentials = Depends(http_bearer)):
    token = creds.credentials
    if token := users.get(token):
        return token
    raise HTTPException(status_code=401, detail="not auth")


# @router.get("/me")
# async def get_me(payload: AuthUserDep):
#     return payload
