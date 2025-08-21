from fastapi import FastAPI,APIRouter,File,UploadFile,HTTPException,Depends
from sqlalchemy.orm import session
from fastapi.responses import JSONResponse
from . import (
    database,
    reset_password,
    schema,
    validation,
    models,
    email_trigger
)
import os

router = APIRouter()

UPLOAD_FOLDER = "image_store"
os.makedirs(UPLOAD_FOLDER,exist_ok=True)

@router.post("/profile/image_upload")
async def profile_image_upload(
    username:str,
    file:UploadFile=File(...),
    otp:str=None,
    db= Depends(database.get_db)
):
    
    if not username:
        raise HTTPException(status_code=404,detail= "Username not found.")
    
    user = db.query(models.user_details).filter(models.user_details.username==username).first()

    if not user:
        raise HTTPException(status_code=404,detail="Username not found.")
    
    if not user.otp==otp:
        raise HTTPException(status_code=404,detail="Invalid Otp.")
    
    _, ext = os.path.splitext(file.filename)
    safe_filename = f"{user.username}{ext}"
    file_path = os.path.join(UPLOAD_FOLDER,safe_filename)

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    return {
        "message": "Profile image uploaded successfully",
        "username": username
    }