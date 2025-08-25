from Event_api.login_page1 import database
from Event_api.login_page1 import password_hashing
from fastapi import Depends,APIRouter, HTTPException
from sqlalchemy.orm import Session
from .event_schema import Event_Creation_Details,Event_Update_Details
from .event_models import event_detail_database
from Event_api.login_page1.models import user_details
from Event_api.login_page1.email_trigger import Verify_user_otp, Verify_otp
from Event_api.login_page1 import schema

router = APIRouter()

@router.post("/Create_event")
def Create_event_process(
    data : Event_Creation_Details,
    db=Depends(database.get_db)
):
    user = db.query(user_details).filter(user_details.username==data.your_username).first()

    if not user :
        raise HTTPException(status_code=404,detail="Username not found.")
    
    if user.user_type != "admin":
        raise HTTPException(status_code=400,detail="only admin can create event.")
    
    otp_verify_method = Verify_user_otp(
        Verify_otp(
            email = user.email,
            otp = data.otp
        ),
        db=db
    )

    new_event = event_detail_database(
        event_created_by = data.your_username,
        event_name = data.event_name,
        event_description = data.event_description,
        event_date = data.event_date,
        event_time = data.event_time,
        event_location = data.event_location,
        event_price = data.event_price
    )
    db.add(new_event)
    db.commit()
    db.refresh(new_event)

    return {"Message":f"Event created successfully, Event ID : {new_event.event_id}."}
    
@router.post("/Update_event")
def event_update_process (
    data : Event_Update_Details,
    db: Session = Depends(database.get_db)
):
    user = db.query(user_details).filter(user_details.username==data.your_username).first()

    if not user :
        raise HTTPException(status_code=404,detail="Username not found.")
    
    if user.user_type != "admin":
        raise HTTPException(status_code=400,detail="only admin can update event details.")
    
    otp_verify_method = Verify_user_otp(
        Verify_otp(
            email = user.email,
            otp = data.otp
        ),
        db=db
    )
    event = db.query(event_detail_database).filter(event_detail_database.event_id==data.event_id).first()

    if not event :
        raise HTTPException (status_code = 404, detail = "Event ID invalid, Please enter correct event id.")

    if data.event_name != "string":
        event.event_name = data.event_name

    if data.event_description != "string":
        event.event_description = data.event_description

    if data.event_date != "string" :
        event.event_date = data.event_date

    if data.event_time != "string":
        event.event_time = data.event_time
    
    if data.event_location != "string" :
        event.event_location = data.event_location

    if data.event_price != 0 :
        event.event_price = data.event_price

    event.event_updated_by = data.your_username

    db.commit()
    db.refresh(event)

    return {"Message":"Event Updated Successfully."}