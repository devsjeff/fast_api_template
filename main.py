from fastapi import FastAPI
import asyncio
from secure import verify_password , create_access_token, verify_jwt 
from schema import Login, password , make_password ,Email , TOKEN
from Mail import send_email , verify_otp
from database import insert_user , get_user_password

app = FastAPI()

@app.post("/otp")
async def get_otp(email_object: Email):
    send_email(email_object.email)
    return {"message":"OTP sent successfully"}

@app.post("/reset_password")
async def home(object:make_password):
    if verify_otp(object.email, object.otp):
        # hashed_password = hash_password(object.password)
        insert_user(object.email, object.password)
        return {"message":"Password reset successful"}
    return {"message":"Invalid OTP "}
@app.post("/login")
async def login(object:Login):
    if verify_password(get_user_password(object.email), object.password):
        
        return {"message":"Login successful" ,"token":create_access_token(object.email) }
    return {"message":"Invalid email or password"}

@app.post("/posts")
async def posts(TOKEN:TOKEN):
    if verify_jwt(token=TOKEN.token):
        return "here is your 570 posts"
    else:
        "WRONG DETAILS"