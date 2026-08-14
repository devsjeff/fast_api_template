import argon2
from datetime import datetime, timedelta, timezone
from jose import jwt ,JWTError
hasher = argon2.PasswordHasher()
from schema import JWT_verify
import os
from dotenv import load_dotenv
load_dotenv()
SECRET_KEY :str = os.getenv("SECRET_KEY")
if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing")
ALGORITHM : str = os.getenv("ALGORITHM")


def hash_password(password: str) -> str:
    return hasher.hash(password)

def verify_password( hashed_password: str ,password: str) -> bool:
    try:
        return hasher.verify(hashed_password, password)
    except argon2.exceptions.VerifyMismatchError:
        return False



def create_access_token(email ):
    expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    payload = {"sub": email, "exp": expire}
    return jwt.encode(payload,SECRET_KEY,algorithm=ALGORITHM) 

def verify_jwt( token ):
    try :
        jwt.decode(token=token , key = SECRET_KEY , algorithms=[ALGORITHM]) 
        return True
    except JWTError:
        return False
        