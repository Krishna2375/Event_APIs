from fastapi import APIRouter,HTTPException,Depends
from sqlalchemy.orm import Session
from Event_api.login_page1 import database,models,email_trigger
from . import event_schema,event_models

router = APIRouter()

@router.delete("/delete_event/")
def delete_event (data : event_schema.Delete_event_schema , db : Session = Depends(database.get_db)):
    event_detail = db.query(event_models.event_detail_database).filter(
        event_models.event_detail_database.event_id == data.event_id
    ).first()
    
    if not event_detail :
        raise HTTPException(status_code=404,detail = "Event ID not found.")
    
    user_detail = db.query(models.user_details).filter(models.user_details.username == data.username).first()
    if not user_detail :
        raise HTTPException(status_code=404, detail="User not found.")
    
    if user_detail.user_type != "admin":
        raise HTTPException(status_code=400,detail="Admin can delete event.")
    
    otp_verify_for_delete = email_trigger.Verify_user_otp(
        email_trigger.Verify_otp(
            email = user_detail.email,
            otp = data.otp
        ),
        db = db
    )
    
    db.delete(event_detail)
    db.commit()

    return {"Message" : "Event delete successfully"}