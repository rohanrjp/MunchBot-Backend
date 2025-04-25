from fastapi import Depends
from typing import Annotated
from ..services.auth_services import get_current_user

user_dependancy=Annotated[dict,Depends(get_current_user)]  