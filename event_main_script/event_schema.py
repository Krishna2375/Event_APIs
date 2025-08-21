from pydantic import BaseModel, ConfigDict
from datetime import datetime

class Event_Creation_Details(BaseModel):
    your_username : str
    event_name : str
    event_description : str
    event_date : str
    event_time : str
    event_location : str
    event_price :int
    otp : str 

class Event_Update_Details(BaseModel):
    your_username : str
    event_id : int
    event_name : str | None
    event_description : str | None
    event_date : str | None
    event_time : str | None
    event_location : str | None
    event_price :int | None
    otp : str

    class Config:
        from_attributes = True

class verify_otp(BaseModel):
    email: str
    otp : str

class Ticket_booking_schema (BaseModel):
    username : str
    event_name : str
    number_of_seat : int
    otp : str 

class Event_list_out (BaseModel):
    event_id : int
    event_name : str
    event_description : str
    event_date : str
    event_time : str
    event_location : str
    event_price : int
    event_seats_remaining : int
    event_seats_closed : int

    model_config = ConfigDict(from_attributes=True)

class Booking_history_out (BaseModel):
    id: int
    username: str
    email: str
    mobile_no: int
    name: str
    ticket_booked_at: datetime
    event_name : str
    event_id : int

    model_config = ConfigDict(from_attributes=True)

class Delete_event_schema (BaseModel):
    username : str
    event_id : int
    otp : str

class cancel_booking (BaseModel):
    id : int 
    otp : str
    
class excel_sheet_request (BaseModel):
    username : str
    otp : str
    event_id : int