from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from fastapi.responses import FileResponse
import pandas as pd
from . import event_models,event_schema
from Event_api.login_page1 import database, models , validation, email_trigger

router = APIRouter()

@router.post("/get_event_booked_list_excel")
async def event_excel (data:event_schema.excel_sheet_request,db:Session=Depends(database.get_db)):

    event_detail = db.query(event_models.Event_seat_details).filter(
        event_models.Event_seat_details.event_id == data.event_id
    ).all()
    
    if not event_detail : 
        raise HTTPException(status_code=404,detail="Event detail not found.")
    
    user_data = db.query(models.user_details).filter(
        models.user_details.username==data.username
    ).first()

    if not user_data :
        raise HTTPException(status_code=404,detail="Username not found.")
    
    if user_data.user_type != "admin" :
        return {"Message":"Only admin can get excel data of event booking list."}
    
    otp_verify_process =email_trigger.Verify_user_otp(
        email_trigger.Verify_otp(
            email = user_data.email,
            otp = data.otp
        ),
        db=db
    )
    
    event_ticket_booked_detail = [
        {
            "username" : e.username,
            "event_id" : e.event_id,
            "event_name" : e.event_name,
            "seat_no" : e.seat_no,
        }
        for e in event_detail
    ]

    df = pd.DataFrame(event_ticket_booked_detail)

    file_path = "event_ticket.xlsx"

    df.to_excel(file_path, index=False)

    return FileResponse(
        path=file_path,
        filename="events.xlsx",
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )