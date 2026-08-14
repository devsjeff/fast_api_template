from fastapi import FastAPI , Request
from slowapi import Limiter , _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
import asyncio
from secure import verify_password , create_access_token, verify_jwt 
from schema import Login, password , make_password ,Email , TOKEN
from Mail import send_email , verify_otp
from database import insert_user , get_user_password

app = FastAPI()

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded , _rate_limit_exceeded_handler)

@app.post("/otp")
@limiter.limit("5/minute")
async def get_otp( email_object: Email ,request: Request):
    send_email(email_object.email)
    return {"message":"OTP sent successfully"}

@app.post("/reset_password")
@limiter.limit("5/minute")
async def home( object:make_password ,request: Request ):
    if verify_otp(object.email, object.otp):
        # hashed_password = hash_password(object.password)
        insert_user(object.email, object.password)
        return {"message":"Password reset successful"}
    return {"message":"Invalid OTP "}


@app.post("/login")
@limiter.limit("5/minute")
async def login(object:Login  ,request: Request):
    if verify_password(get_user_password(object.email), object.password):
        
        return {"message":"Login successful" ,"token":create_access_token(object.email) }
    return {"message":"Invalid email or password"}

@app.post("/posts")
@limiter.limit("5/minute")
async def posts(TOKEN:TOKEN ,request:Request):
    if verify_jwt(token=TOKEN.token):
        return "here is your 570 posts"
    else:
        return "WRONG DETAILS"
    
@app.get("/slow")
@limiter.limit("3/minute")

async def get (request:Request):
    return "non blocked"
    