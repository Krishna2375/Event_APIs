import os 
from dotenv import load_dotenv
from email.message import EmailMessage
from datetime import datetime , timedelta
from sqlalchemy.orm import session
import aiosmtplib
import random
from .models import user_details
from .schema import EmailRequest,Verify_otp
from fastapi import APIRouter,HTTPException, BackgroundTasks,Depends
from .database import get_db

router = APIRouter()
load_dotenv()

EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
EMAIL_USER = os.getenv("EMAIL_USER")
EAMIL_PASS = os.getenv("EMAIL_PASS")

async def sent_otp_email (to_email:str,otp:str):
    message = EmailMessage()
    message["From"]=EMAIL_USER
    message["To"]=to_email
    message["subject"]="Your OTP Code"
    message.set_content(f"Your OTP Code is {otp}, this valid for 10 minutes.")

    await aiosmtplib.send(
        message,
        hostname = EMAIL_HOST,
        port = EMAIL_PORT,
        start_tls=True,
        username=EMAIL_USER,
        password=EAMIL_PASS
    )

@router.post("/Email/sent_otp")
async def sent_otp(username:str,backgroundtasks:BackgroundTasks,db:session=Depends(get_db)):
    otp = random.randint(100000,999999)
    otp_expiry_time =datetime.utcnow()+timedelta(minutes=10)
    user = db.query(user_details).filter(user_details.username==username).first()
    if not user :
        raise HTTPException(status_code= 404, detail="User not found.")
    
    user.otp=otp
    user.otp_expiry=otp_expiry_time
    db.commit()

    backgroundtasks.add_task(sent_otp_email,user.email,otp)

    return {"Message":f"OTP send to {user.email}"}


async def sent_otp_for_reset (email:str,backgroundtasks:BackgroundTasks,db:session=Depends(get_db)):
    otp = random.randint(100000,999999)
    otp_expiry_time =datetime.utcnow()+timedelta(minutes=10)
    user = db.query(user_details).filter(user_details.email==email).first()
    if not user :
        raise HTTPException(status_code= 404, detail="User not found.")
    
    user.password_reset_code=otp
    user.otp_expiry=otp_expiry_time
    db.commit()

    backgroundtasks.add_task(sent_otp_email,user.email,otp)

    return {"Message":f"Password reset code send to {user.email}"}

def Verify_user_otp(data :Verify_otp,db: session=Depends(get_db)):
    user= db.query(user_details).filter(user_details.email==data.email).first()

    if not user:
        raise HTTPException(status_code=404, detail="Username not found")
    try:
        expiry_time = datetime.strptime(user.otp_expiry,"%Y-%m-%d %H:%M:%S.%f")
    except ValueError:
        raise HTTPException(status_code=400,detail="Invalid time format")
    if datetime.utcnow() > expiry_time:
        raise HTTPException(status_code=400,detail="OTP Has Expired")
    if data.otp != user.otp:
        raise HTTPException(status_code=400,detail="Invalid OTP")
    return {"message": "OTP verified successfully"}