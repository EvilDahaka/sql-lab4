from fastapi import APIRouter, HTTPException
from auth.dependencies import UserServiceDep
from auth.schemas import UserLogin, UserRegister, UserResponce, TokenSchemas

router = APIRouter(tags=["users"])


@router.get("/users/{user_id}")
async def get_user(user_id: int, user_servise: UserServiceDep) -> UserResponce:
    user = await user_servise.get(user_id)
    if not user:
        raise HTTPException(status_code=400, detail="Користувача не існує")
    return user


@router.post("/register")
async def reg_user(data: UserRegister, user_service: UserServiceDep) -> TokenSchemas:
    try:
        user = await user_service.register(data)
        if not user:
            raise HTTPException(status_code=400, detail="Користувача з такой поштой існує")
        return user
    except ValueError:
        raise HTTPException(status_code=400, detail="Користувача з такой поштой існує")


@router.post("/login")
async def login(user: UserLogin, user_servise: UserServiceDep) -> TokenSchemas:
    token = await user_servise.login(user)
    if not token:
        raise HTTPException(400, "Невірний логін чи пароль")
    return token
