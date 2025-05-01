from typing import Annotated
from app.database import SessionLocal
from ..schemas.auth_schemas import UserSignUp
from sqlalchemy.orm import Session    
from ..models.auth_models import User
from ..utils import hash_password,convert_utc_to_ist
from pydantic import EmailStr
from ..exceptions.auth_exceptions import Invalid_Credentials_Exception
import uuid
from datetime import timedelta,datetime,timezone
import jwt
from ..config import settings
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends,WebSocket,HTTPException,status
from ..dependancies.db_dependencies import db_dependancy
from jwt.exceptions import PyJWTError

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="/auth/login")

def check_user_exits(new_user_email:EmailStr,db:Session):
    return db.query(User).filter(new_user_email==User.email).first() 
    
def add_user(new_user: UserSignUp,db:Session)->None:
    current_utc_datetime=datetime.now(timezone.utc)
    current_ist_datetime=convert_utc_to_ist(current_utc_datetime)
    hashed_password=hash_password(new_user.password)
    user=User(
        name=new_user.name,
        email=new_user.email,
        hashed_password=hashed_password,
        joining_date=current_ist_datetime
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise e
    
def create_access_token(client_uuid:uuid.UUID,expiry_time:int|None=None)->str:
    payload={'sub':str(client_uuid),'iat':datetime.now(timezone.utc)}
    if expiry_time is not None:
        payload.update({'exp':datetime.now(timezone.utc)+timedelta(minutes=expiry_time)})
    else:
        payload.update({'exp':datetime.now(timezone.utc)+timedelta(minutes=10)})
        
    return jwt.encode(payload=payload,key=settings.SECRET_KEY,algorithm=settings.ALGORITHM)     
    
def get_current_user(jwt_token:Annotated[str,Depends(oauth2_scheme)],db:db_dependancy):
    try:
        payload=jwt.decode(jwt_token,key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_uuid:uuid.UUID=payload.get('sub')
        if user_uuid is None:
            raise Invalid_Credentials_Exception
        user=db.query(User).filter(User.uuid==user_uuid).first()
        if not user:
            raise Invalid_Credentials_Exception
        return user
    except PyJWTError:
        raise Invalid_Credentials_Exception
    

async def get_current_user_websocket(websocket:WebSocket,db: Session):
    
    jwt_token=websocket.query_params.get('token')
    if not jwt_token:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="Invalid token or missing token")
    
    try:
        payload=jwt.decode(jwt_token,key=settings.SECRET_KEY,algorithms=[settings.ALGORITHM])
        user_uuid=payload.get('sub')
        if not user_uuid:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise Invalid_Credentials_Exception
        user=db.query(User).filter(User.uuid==user_uuid).first()
        
        if not user:
            await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
            raise Invalid_Credentials_Exception
        
        return user
    except PyJWTError:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        raise Invalid_Credentials_Exception
        
        