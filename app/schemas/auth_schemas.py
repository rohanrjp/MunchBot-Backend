from pydantic import BaseModel,Field,EmailStr

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