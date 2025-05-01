from fastapi import Depends
from typing import Annotated
from ..services.auth_services import get_current_user
from ..models.auth_models import User

user_dependancy=Annotated[User,Depends(get_current_user)]  