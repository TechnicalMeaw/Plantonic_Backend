from fastapi import status, HTTPException, Depends, APIRouter
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..blue_dart import api as bd


router = APIRouter(prefix= "/deliver",
                   tags=["Delivery"])

@router.get("/check_pin_code", response_model = schemas.PinCodeAvailibility)
def check_pin_code(pincode: str, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    
    if not utils.is_valid_pin_code(pincode):
        HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid pin code')

    if not bd.check_pin_code_availability(pincode):
        HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Delivery at this pin code is not available')
    
    return {"is_delivery_possible": True, "detail": ""}
   
        