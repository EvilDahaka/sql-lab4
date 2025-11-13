from functools import wraps
from fastapi import APIRouter, HTTPException, Response, status
from src.auth.exceptions import InvalidRefreshToken, RegistrationError, LoginError
from src.auth.schemas import UserRegister, UserLogin, TokenSchemas, LoginResponce
from src.auth.dependencies import AuthServiceDep
from fastapi import APIRouter, HTTPException, Depends
from src.auth.dependencies import UserServiceDep
from src.auth.exceptions import UserRegistrationError
from src.auth.schemas import UserLogin, UserRegister, UserResponce, TokenSchemas
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth",tags=['Auth']) # type: ignore[misc]

def check_invalid_refresh_token(func): 
    @wraps(func) 
    async def wrapper(*args, **kwargs): 
        try: 
            result = await func(*args, **kwargs) 
        except InvalidRefreshToken: 
            raise HTTPException(status_code=403, detail="Invalid refresh token.") 
        return result 
    return wrapper

@router.post("/register")
async def register_user(data: UserRegister, service: AuthServiceDep)-> LoginResponce:
    try:
        user = await service.register(data)
    except RegistrationError:
        raise HTTPException(
            status_code=400, detail="A user with this email address exists."
        )
    return user


@router.post("/login")
async def login(user: UserLogin, service: AuthServiceDep) -> LoginResponce:
    try:
        token = await service.login(user)
    except LoginError:
        raise HTTPException(status_code=400, detail="Invalid email or password.")
    return token


@router.post("/refresh")
@check_invalid_refresh_token
async def refresh_token(refresh_token: str, service: AuthServiceDep) -> TokenSchemas:
    token = await service.refresh(refresh_token)
    return token


@router.post("/logout")
@check_invalid_refresh_token
async def logout(refresh_token: str, service: AuthServiceDep):
    await service.logout(refresh_token)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
'''
@router.post("/login")
async def login(user: UserLogin, user_servise: UserServiceDep) -> TokenSchemas:
    token = await user_servise.login(user)
    if not token:
        raise HTTPException(400, "Невірний логін чи пароль")
    return token
'''



@router.post("/login")
async def login(
    user_servise: UserServiceDep, 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> TokenSchemas:
    
    
    user_data = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    
   
    token = await user_servise.login(user_data) 
    
    if not token:
        raise HTTPException(400, "Невірний логін чи пароль")
    return token
