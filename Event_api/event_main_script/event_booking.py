from fastapi import Depends,APIRouter,HTTPException
from sqlalchemy.orm import Session
from .event_schema import Ticket_booking_schema
from . import event_models
from Event_api.login_page1 import (
    database,
    schema,
    email_trigger,
    models,
    password_hashing,
    reset_password,
    validation
)

router = APIRouter()

@router.post("/ticket_booking")
def ticket_booking(
    data : Ticket_booking_schema,
    db : Session = Depends(database.get_db)
):
    user_detail = db.query(models.user_details).filter(models.user_details.username==data.username).first()
    if not user_detail :
        raise HTTPException(status_code=404,detail="Username not found.")
    
    event_detail = db.query(event_models.event_detail_database).filter(event_models.event_detail_database.event_name == data.event_name).first()
    if not event_detail :
        raise HTTPException(status_code=404, detail="Event name not found.")
    
    otp_verify_method = email_trigger.Verify_user_otp(
        email_trigger.Verify_otp(
            email = user_detail.email,
            otp = data.otp
        ),
        db=db
    )

    seat_no_start = event_detail.event_seats_closed+1
    seat_no_end = event_detail.event_seats_closed+data.number_of_seat

    new_ticket_booking_detail = event_models.Event_ticket_booking(
        username = data.username,
        email = user_detail.email,
        mobile_no = user_detail.mobile_no,
        name = user_detail.name,
        event_name = event_detail.event_name,
        event_id = event_detail.event_id
    )

    new_seat_booking = event_models.Event_seat_details(
        username = data.username,
        event_id = event_detail.event_id,
        event_name = event_detail.event_name,
        seat_no = f"{seat_no_start}-{seat_no_end}"
    )
    db.add(new_ticket_booking_detail)
    db.add(new_seat_booking)

    event_detail.event_seats_remaining -= data.number_of_seat
    event_detail.event_seats_closed += data.number_of_seat


    db.commit()
    db.refresh(new_seat_booking)
    db.refresh(new_ticket_booking_detail)

    return {"Message" : "Ticket Booked Successfully",
            "event_id" : event_detail.event_id,
            "seat_no":f"{new_seat_booking.seat_no}"}