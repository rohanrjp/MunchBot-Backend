from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash_password(input_password:str)->str:
    return pwd_context.hash(input_password)    

def verify_password(hashed_password,input_password:str):
    return pwd_context.verify(hashed_password,input_password)