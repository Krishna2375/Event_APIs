from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from . import event_schema,event_models,event_booking,event_creation_update
from Event_api.login_page1 import (
    database,
    schema,
    email_trigger,
    models,
    password_hashing,
    reset_password,
    validation
)

router =APIRouter()

@router.get("/All_event_list",response_model=list[event_schema.Event_list_out])
def event_all_list(db : Session = Depends(database.get_db)):
    event_details = db.query(event_models.event_detail_database).all()
    
    return event_details

@router.post("/event_detail{event_id}")
def single_event (event_id : str , db : Session = Depends(database.get_db)):
    event_detail = db.query(event_models.event_detail_database).filter(event_models.event_detail_database.event_id == event_id).first()
    
    if not event_detail :
        raise HTTPException(status_code=404,detail="Event ID not found.")
    
    return {
            "id": event_detail.event_id,
            "event_name": event_detail.event_name,
            "event_description": event_detail.event_description,
            "event_date": event_detail.event_date,
            "event_time": event_detail.event_time,
            "event_location": event_detail.event_location,
            "event_price": event_detail.event_price,
            "event_seats_remaining": event_detail.event_seats_remaining,
        }