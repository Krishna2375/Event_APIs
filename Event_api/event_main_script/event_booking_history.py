from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from Event_api.login_page1 import database,models,schema
from . import event_models, event_schema

router = APIRouter()

@router.get("/booking_history/{username}",response_model=list[event_schema.Booking_history_out])
def user_booking_history (username : str, db:Session=Depends(database.get_db)):
    user_booking = db.query(event_models.Event_ticket_booking).filter(
        event_models.Event_ticket_booking.username == username
    ).all()

    if not user_booking :
        raise HTTPException (status_code=404, detail="User booking details not found.")
    
    return user_booking