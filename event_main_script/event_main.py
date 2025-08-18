from fastapi import FastAPI,HTTPException,Depends,APIRouter
from sqlalchemy.orm import session
from login_page.database import get_db, Base,engine
from .event_schema import Event_Creation_Details, Event_Update_Details

router = APIRouter()

Base.metadata.create_all(bind=engine)

# @router.get("/summa")
# def summa ():
#     print("hi")
#     return {"Message":"Hi"}