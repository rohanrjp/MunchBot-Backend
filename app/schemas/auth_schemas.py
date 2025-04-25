from pydantic import BaseModel,Field,EmailStr
from datetime import datetime

class UserSignUp(BaseModel):
    name:str=Field(min_length=2,max_length=20)
    email:EmailStr
    password:str=Field(min_length=8)
    
class UserLogIn(BaseModel):
    email:EmailStr
    password:str=Field(min_length=8)
    
class Token(BaseModel):
    access_token:str 
    token_type:str   
    
class UserProfile(BaseModel):
    name:str
    email:str       
    joining_date:datetime 