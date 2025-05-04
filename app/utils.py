from passlib.context import CryptContext
from datetime import datetime,timedelta, timezone

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(input_password:str)->str:
    return pwd_context.hash(input_password)    

def verify_password(hashed_password:str,input_password:str)->bool:
    return pwd_context.verify(input_password,hashed_password)

def convert_utc_to_ist(utc_time:datetime)->datetime:
    ist_delta=timedelta(hours=5,minutes=30)
    ist_timezone=timezone(ist_delta)
    return (utc_time+ist_delta).replace(tzinfo=ist_timezone)