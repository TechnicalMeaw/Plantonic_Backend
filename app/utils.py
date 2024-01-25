from passlib.context import CryptContext
from datetime import datetime, timedelta
import requests
from sqlalchemy.orm import Session
from . import models
import re
import time as T
import indiapins


pwd_context = CryptContext(schemes=["bcrypt"], deprecated = "auto")

def hash(password : str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def split_phone_number(phone_number):
    pattern = r'^(\+\d{1,3})(\d{10})$'
    match = re.match(pattern, phone_number)
    if match:
        country_code = match.group(1)
        number = match.group(2)
        return country_code, number
    else:
        return None, None
    
def is_valid_pin_code(pinCode:str):
    # Regex to check valid pin code
    # of India.
    regex = "^[1-9]{1}[0-9]{2}\\s{0,1}[0-9]{3}$" 
    p = re.compile(regex)
     
    if (pinCode == ''):
        return False

    m = re.match(p, pinCode)
    if m is None:
        return False
    else:
        return True
    

def current_milli_time():
    return round(T.time() * 1000)

def get_pickup_date():
    # Puckup date
    current_date = datetime.now().date()
    # Calculate the date for day after tomorrow
    day_after_tomorrow = current_date + timedelta(days=2)
    # Combine the date for day after tomorrow with 4 pm time
    desired_time = datetime.combine(day_after_tomorrow, datetime.strptime('16:00', '%H:%M').time())
    return int(desired_time.timestamp() * 1000)


def get_location_details(pincode: str):
    maches = indiapins.matching(pincode)
    result = []
    for each in maches:
        temp = {}
        temp['name'] = each['Name']
        temp['region'] = each['Region'].replace(" Region", "")
        temp['dist'] = each['District']
        temp['state'] = each['State']
        temp['country'] = each['Country']
        temp['pin'] = str(each['Pincode'])
        result.append(temp)
    return result