from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from Event_api.login_page1.database import Base

class event_detail_database(Base):
    __tablename__="event_detail_database"

    event_id = Column(Integer,primary_key=True,index=True)
    event_name = Column(String,unique=True,index=True)
    event_description = Column(String)
    event_date = Column(String)
    event_time = Column(String)
    event_location = Column(String)
    event_price = Column(Integer)
    event_seats_remaining = Column(Integer,default=100)
    event_seats_closed = Column(Integer,default=0)
    event_created_at = Column(DateTime,default=datetime.utcnow)
    event_updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    event_created_by = Column(String,nullable=False)
    event_updated_by = Column(String,nullable=True)

class Event_ticket_booking(Base):
    __tablename__ = "user_ticket_booked_details"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True,nullable=False)
    email = Column(String,unique=True,index=True,nullable=False)
    mobile_no = Column(Integer,unique=True,index=True)
    name = Column(String)
    event_name = Column(String,index=True)
    event_id = Column(Integer,index=True)
    ticket_booked_at = Column(DateTime,default=datetime.utcnow)
    ticket_updated_at = Column(DateTime,default=datetime.utcnow)

class Event_seat_details(Base):
    __tablename__ = "event_seat_detail"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,index= True)
    event_id = Column(Integer,index=True)
    event_name = Column(String,index=True)
    seat_no = Column(String)
    seat_booked_at = Column(DateTime,default=datetime.utcnow)