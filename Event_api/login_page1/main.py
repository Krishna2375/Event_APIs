from fastapi import FastAPI,Depends,HTTPException
from .database import Base , engine,get_db
from .update import user_details_update
from . import schema,models, password_hashing, email_trigger
from .email_trigger import Verify_user_otp
from .schema import Verify_otp
from . import reset_password,upload_image
from event_main_script import event_creation_update, event_main, event_booking,event_list,event_delete,event_booking_history,event_booking_cancel

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(user_details_update.router,tags=["User"])
app.include_router(email_trigger.router, tags=["Email_OTP"])
app.include_router(reset_password.router, tags=["Password_Reset"])
app.include_router(upload_image.router, tags=["Image_upload"])
#app.include_router(event_main.router, tags=["Event_Booking"])
app.include_router(event_creation_update.router, tags=["Create_Event"])
app.include_router(event_booking.router, tags=["Event_Booking"])
app.include_router(event_list.router, tags=["Event_details"])
app.include_router(event_delete.router, tags=["Event_delete"])
app.include_router(event_booking_history.router, tags=["Booking_history"])
app.include_router(event_booking_cancel.router, tags=["Booking_cancel"])

def login_status_teller():
    return login_status

@app.post("/login")
def user_login(user:schema.User_Login,db=Depends(get_db)):
    global login_status
    login_status = False
    login_user_data = db.query(models.user_details).filter(models.user_details.email == user.email).first()
    if not login_user_data or not password_hashing.verify_password(user.password,login_user_data.password):
        raise HTTPException(status_code=404, detail="Invalid useremail or password")
    otp_verify_call = Verify_user_otp(
        Verify_otp(email=user.email,
        otp=user.otp),
        db=db
    )
    token = password_hashing.create_access_token({"sub":login_user_data.username,"user_type":login_user_data.user_type})
    login_status = True
    return {"Message" : "Login Successfully",
            "Access_token":token,
            "Token":"bearer"}

@app.post("/signup")
def user_signup(user:schema.User_Signup,db=Depends(get_db)):
    existing_user_check = db.query(models.user_details).filter(models.user_details.username == user.username).first()
    if existing_user_check:
        raise HTTPException(status_code=404,detail="Invalide username or password")
    hashed_pwd = password_hashing.get_password_hashed(user.password)
    new_user = models.user_details(
        username=user.username,
        password=hashed_pwd,
        email=user.email,
        mobile_no=user.mobile_no,
        name=user.name,
        age=user.age,
        user_type=user.user_type,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    show_user_data = schema.show_user_details_to_user(
        id=new_user.id,
        name=new_user.name,
        age=new_user.age,
        username=new_user.username,
        email=new_user.email,
        mobile_no=new_user.mobile_no,
        created_at=new_user.created_at
        )
    return show_user_data