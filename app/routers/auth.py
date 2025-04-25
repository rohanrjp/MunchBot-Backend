from fastapi import APIRouter,status,HTTPException,Depends
from fastapi.responses import JSONResponse
from ..schemas.auth_schemas import UserSignUp,Token,UserProfile
from ..dependancies.db_dependencies import db_dependancy
from ..dependancies.auth_dependancies import user_dependancy
from ..services.auth_services import add_user,check_user_exits,create_access_token
from ..utils import verify_password
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from ..config import settings

auth_router=APIRouter(prefix="/auth",tags=["Auth"])

@auth_router.post("/sign-up")
async def user_sign_up(new_user:UserSignUp,db:db_dependancy):
    user_exists=check_user_exits(new_user.email,db)
    if user_exists:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User with the same email exists")
    else:
        add_user(new_user,db)
        return JSONResponse(content={"detail":"User created"},status_code=status.HTTP_201_CREATED)


@auth_router.post("/login")
async def user_log_in(db:db_dependancy,form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    existing_user=check_user_exits(form_data.username,db)
    if not existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="User not found")
    if not verify_password(existing_user.hashed_password,form_data.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Password entered for this user is wrong")
    else:
        jwt_token=create_access_token(existing_user.uuid,settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        return Token(access_token=jwt_token,token_type="bearer") 
    
@auth_router.get('/profile',response_model=UserProfile,status_code=status.HTTP_200_OK)
async def get_current_user(user:user_dependancy):
    return user
           
        
    
        