from pydantic import field_validator
import re

def username_validation (value:str)->str:
    if " " in value:
        raise ValueError ("Username not allowed to have space.")
    if not value.islower():
        raise ValueError ("Username Most been in small letters only.")
    if len(value) <4:
        raise ValueError("username must be greater than 4 letter.")
    if len(value)>60:
        raise ValueError("Username must be less than 60")
    return value
    
def password_validation (value:str)->str:
    if (not re.search(r"[A-Z]",value)or
        not re.search(r"[a-z]",value)or
        not re.search(r"[0-9]",value)or
        not re.search(r"[A-Za-z0-9]",value)):
        raise ValueError("Password must include 1 uppercase, 1 lowercase, and 1 special character")
    return value
    
def email_validation (value:str)->str:
    if not value.endswith("@gmail.com"):
        raise ValueError("Email must be a Gmail address.")
    return value
        
def mobile_no_validation (value:str)->str:
    if len(value)!= 10 or not value.isdigit():
        raise ValueError("Mobile must be 10 digit.")
    return value
    
def name_validation (value:str)->str:
    if re.search(r"[0-9]",value):
        raise ValueError("Name only allowed in letters not in numbers.")
    return value
    
def age_validation (value:str)->str:
    try:
        age_in_int = int(value)
    except ValueError:
        raise ValueError("Age must be number.")
    if age_in_int < 18 :
        raise ValueError("Age must be 18.")
    return value

def user_type_validation (value:str)->str:
    user_type_list = ["user","admin"]
    if value not in user_type_list:
        raise ValueError("Only user and admin are allowed.")
    return value