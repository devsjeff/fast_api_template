import smtplib
import random
from email.message import EmailMessage
from dotenv import load_dotenv
import os
from datetime import datetime  , timedelta , timezone
import redis

load_dotenv()
redis_db = redis.Redis(host='localhost', port=6379, db=0)

EMAIL = os.getenv("EMAIL")
PASSWORD = os.getenv("PASSWORD")

def send_email(email):
    msg = EmailMessage()
    msg['From'] = EMAIL
    msg['To'] = email
    msg['Subject'] = "Test Email"
    OTP = random.randint(100000,999999)
    msg.set_content(f"OTP = {OTP}")
    with smtplib.SMTP_SSL("smtp.gmail.com" , 465) as smtp:
        smtp.login(user=EMAIL , password=PASSWORD)
        smtp.send_message(msg)
    redis_db.set(email, OTP , ex=300) 

def verify_otp(email, otp):
    stored_otp = redis_db.get(email)
    if stored_otp is None:
        return False
    result = stored_otp.decode() == otp
    redis_db.delete(email)
    return result