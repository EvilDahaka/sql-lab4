from typing import Annotated

from fastapi import Depends

from auth.service import UserService, get_user_servise


UserServiceDep = Annotated[UserService, Depends(get_user_servise)]
