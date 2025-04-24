from ..schemas.auth_schemas import UserSignUp
from sqlalchemy.orm import Session    
from ..models.auth_models import User
from ..utils import hash_password
from pydantic import EmailStr
from ..utils import pwd_context

def check_user_exits(new_user_email:EmailStr,db:Session):
    return db.query(User).filter(new_user_email==User.email).first() 
    
def add_user(new_user: UserSignUp,db:Session)->None:
    hashed_password=hash_password(new_user.password)
    user=User(
        name=new_user.name,
        email=new_user.email,
        hashed_password=hashed_password
    )
    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except Exception as e:
        db.rollback()
        raise e
    
def create_access_token():
   pass     
    