from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from . import event_models,event_schema
from Event_api.login_page1 import database,email_trigger,models

router = APIRouter()

@router.post("/Cancel_booking/")
def user_cancel_booking (data:event_schema.cancel_booking , db : Session = Depends(database.get_db)):
    user_booking = db.query(event_models.Event_ticket_booking).filter(
        event_models.Event_ticket_booking.id == data.id
    ).first()

    if not user_booking :
        raise HTTPException(status_code=404,detail="Booking ID not found.")
    
    user_otp_verify = email_trigger.Verify_user_otp(
        email_trigger.Verify_otp(email = user_booking.email,
        otp = data.otp),
        db=db
    )
    
    db.delete(user_booking)
    db.commit()

    return {"Message" : "Booking canceled successfully."}

