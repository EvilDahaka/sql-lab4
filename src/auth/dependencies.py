from typing import Annotated

from fastapi import Depends

from src.auth.interface import IAuthService
from src.auth.service import get_user_servise


AuthServiceDep = Annotated[IAuthService, Depends(get_user_servise)]
