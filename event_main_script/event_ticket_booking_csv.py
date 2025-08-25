from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
from . import event_schema, event_models
from Event_api.login_page1 import database,models,email_trigger
import pandas as pd
import io
import csv

router = APIRouter()

@router.post("/get_event_booked_list_csv")
async def event_csv (
    data : event_schema.csv_request,
    db : Session = Depends(database.get_db)
):
    event_detail = db.query(event_models.Event_seat_details).filter(
        event_models.Event_seat_details.event_id == data.event_id
    ).all()

    if not event_detail : 
        raise HTTPException (status_code=404, detail = "Event Booking Detail Not Found.")
    
    user_detail = db.query(models.user_details).filter(
        models.user_details.username == data.username 
    ).first()

    if not user_detail :
        raise HTTPException (status_code=404, detail = "Username not found in the database.")
    
    if user_detail.user_type != "admin" :
        return {"Message" : "Only Admin can access this details."}

    opt_verify_process = email_trigger.Verify_user_otp(
        email_trigger.Verify_otp(
            email = user_detail.email,
            otp = data.otp
        ),
        db = db
    )

    event_ticket_booking_detail = [
        {
            "username" : e.username,
            "event_id" : e.event_id,
            "event_name" : e.event_name,
            "seat_no" : e.seat_no,
        }
        for e in event_detail
    ]

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=["username", "event_id", "event_name", "seat_no"])
    writer.writeheader()
    writer.writerows(event_ticket_booking_detail)

    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=event_{data.event_id}_bookings.csv"}
    )