from . import(
    database,
    email_trigger,
    main,
    models,
    password_hashing,
    schema,
    validation
)
from sqlalchemy.orm import Session
from fastapi import APIRouter,HTTPException,Depends,BackgroundTasks
from datetime import datetime


router = APIRouter()

@router.post("/reset/reset_password_code")
async def reset_password_process(
    data:schema.reset_password_schema,
    backgroundtasks: BackgroundTasks,
    db:Session=Depends(database.get_db)
    ):
    user_data = db.query(models.user_details).filter(models.user_details.email==data.email).first()

    if not user_data :
        raise HTTPException (status_code= 404, detail="Email ID not found.")
    
    # password_check = password_hashing.get_password_hashed(data.password)

    # if not password_hashing.verify_password(data.password,user_data.password):
    #     raise HTTPException(status_code=404, detail="Current Password is Invalid.")
    
    otp_verify_for_reset_password = email_trigger.Verify_user_otp(
        schema.Verify_otp(email=data.email,otp=data.otp),
        db=db
    )

    await email_trigger.sent_otp_for_reset(data.email, backgroundtasks ,db)

    return {"Message" : f"Password Reset Code Send to {user_data.email}"}


@router.post("/reset/change_password")
async def change_password_process(
    data:schema.change_password,
    backgroundtasks:BackgroundTasks,
    db:Session=Depends(database.get_db)
    ):
    user_data = db.query(models.user_details).filter(models.user_details.email==data.email).first()

    if not user_data:
        raise HTTPException(status_code=404,detail="Email ID not found.")

    if not user_data.password_reset_code == data.reset_code:
        raise HTTPException(status_code=400,detail="Reset code is invalid.")
    
    if user_data.otp_expiry:
        try :
            otp_expiry_time_format = datetime.strptime(user_data.otp_expiry, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            raise HTTPException(status_code=500, detail="Invalid expiry format in database.")
        
        if datetime.utcnow() > otp_expiry_time_format:
            raise HTTPException(status_code=400,detail="Reset code has expired.")
    
    if not data.new_password == data.confirm_password:
        raise HTTPException(status_code=400,detail="New Password and confirm password are not same.")
    
    validation.password_validation(data.new_password)

    new_password_change = password_hashing.get_password_hashed(data.new_password)

    user_data.password = new_password_change

    user_data.password_reset_code = None

    db.commit()
    return {"Message" : "Your password changed successfully."}