from pydantic import BaseModel
class password(BaseModel):
    password:str
    
class make_password(BaseModel):
    email:str
    otp:str
    password:str
    
class Email(BaseModel):
    email:str
    
class Login(BaseModel):
    email:str
    password:str