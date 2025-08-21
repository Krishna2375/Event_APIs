from sqlalchemy import Column,String,Integer,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class user_details(Base):
    __tablename__="user_details"

    id = Column(Integer,primary_key=True,index=True)
    username = Column(String,unique=True,index=True)
    password = Column(String)
    email = Column(String,index=True)
    mobile_no = Column(String,index=True)
    name = Column(String)
    age = Column(String)
    user_type = Column(String)
    created_at = Column(DateTime,default=datetime.utcnow)
    updated_at = Column(DateTime,default=datetime.utcnow,onupdate=datetime.utcnow)
    active_status = Column(String,default="active",index=True)
    otp = Column(String,nullable=True)
    otp_expiry = Column(String,nullable=True)
    password_reset_code = Column(String,nullable=True)
