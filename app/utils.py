from passlib.context import CryptContext
from datetime import datetime,timedelta

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(input_password:str)->str:
    return pwd_context.hash(input_password)    

def verify_password(hashed_password:str,input_password:str)->bool:
    return pwd_context.verify(input_password,hashed_password)

def convert_utc_to_ist(utc_time:datetime)->datetime:
    return utc_time+timedelta(hours=5,minutes=30)