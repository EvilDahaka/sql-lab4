from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.auth.auth import get_jwt_codec
from src.auth.schemas import UserResponce as CurrentUserSchema
from .service import get_user_servise, UserService

from fastapi import Depends

from src.auth.interface import IAuthService
from src.auth.service import get_user_servise

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login") 

AuthServiceDep = Annotated[IAuthService, Depends(get_user_servise)]
UserServiceDep = Annotated[UserService, Depends(get_user_servise)]


async def get_current_user(
    user_service: UserServiceDep, 
    token: str = Depends(oauth2_scheme), 
    codec = Depends(get_jwt_codec) 
) -> CurrentUserSchema:
    try:
        payload = codec.decode(token)
        user_id = payload.get("uid")

        if user_id is None:
            raise Exception("Invalid token payload")

        user = await user_service.get(user_id) 

        if user is None:
            raise Exception("User not found")
        
        return user
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недійсні облікові дані або термін дії токена закінчився",
            headers={"WWW-Authenticate": "Bearer"},
        )
