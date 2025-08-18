from fastapi import APIRouter, Depends, HTTPException
from ..schema import Show_User_Update, UpdateUser
from sqlalchemy.orm import session
from ..database import get_db
from ..models import user_details
from pydantic import field_validator
from .. import email_trigger
from ..validation import (
    username_validation,
    password_validation,
    email_validation,
    mobile_no_validation,
    name_validation,
    age_validation,
    user_type_validation
)

router = APIRouter()

@router.put("/User/user_data_update/{email}",response_model=Show_User_Update)
def user_data_update (email :str,updates: UpdateUser,db:session=Depends(get_db)):
    user = db.query(user_details).filter(user_details.email == email).first()
    if not user : 
        raise HTTPException(status_code=404,detail=f"Username : {email} not found.")
    
    if updates.username :
        if not username_validation(updates.username):
            raise HTTPException(status_code=400,detail="Invalid username format.")
        user.username = updates.username

    if updates.name : 
        if not name_validation(updates.name):
            raise HTTPException(status_code=400,detail="Invalid name given.")
        user.name=updates.name

    if updates.email:
        if not email_validation(updates.email):
            raise HTTPException(status_code=400,detail="Invalid email format.")
        user.email = updates.email
        
    if updates.mobile_no:
        if not mobile_no_validation(updates.mobile_no):
            raise HTTPException(status_code=400,detail="Invalid Mobile Number Given.")
        user.mobile_no = updates.mobile_no
        
    if updates.age:
        if not age_validation(updates.age):
            raise HTTPException(status_code=400,detail="Age must be greater than 18..")
        user.age = updates.age
    
    if updates.otp:
        otp_verify_call = email_trigger.Verify_otp(
        email=user.email,
        otp=user.otp
    )

    db.commit()
    db.refresh(user)

    return user