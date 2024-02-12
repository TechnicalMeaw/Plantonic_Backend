from typing import Optional
from fastapi import status, HTTPException, Depends, APIRouter
from datetime import datetime, timedelta
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..firebase import firebase_auth
from ..otp import otp_utils


router = APIRouter(prefix= "/auth",
                   tags=["Authentication"])
                   

@router.post("/", response_model = schemas.Token)
def get_user_token(user : schemas.GetAuthToken, db: Session = Depends(get_db)):
    aes = easyAes.EasyAES()
    # print(user.uid)
    user.uid = aes.decrypt(user.uid)

    print(user.uid)
    local_user = db.query(models.User).filter(models.User.firebase_uid == user.uid).first()

    # IF user doesn't exists locally
    if not local_user:
        # check if user exists on firebase
        firebase_user = firebase_auth.get_firebase_user(user.uid)

        if not firebase_user:
            # if user doesn't exists on firebase
            raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="User doesn't exists")
        else:
            # create local user
            new_user = models.User(firebase_uid = firebase_user["_data"]["localId"], auth_type = firebase_user["_data"]["providerUserInfo"][0]["providerId"])
            db.add(new_user)
            db.commit()
            db.refresh(new_user)

            # create a token
            access_token = oauth2.create_access_token(data=new_user.id)
            return {"access_token": access_token, "token_type": "bearer", "role": aes.encrypt(str(new_user.role))}
    else:
        # update last login
        local_user.last_login = datetime.now()
        db.commit()
        
        # create a token
        access_token = oauth2.create_access_token(data=local_user.id)
        return {"access_token": access_token, "token_type": "bearer", "role": aes.encrypt(str(local_user.role))}


@router.get("/send_otp_to_existing_user")
async def send_otp_to_existing_user(username: str, otp_type: Optional[str] = 'sms', db: Session = Depends(get_db)):
    if utils.is_phone_number(username):
        user = firebase_auth.get_firebase_user_from_phone(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="It seems like you don't have an account with this phone number.")

        local_user = db.query(models.User).filter(models.User.firebase_uid == user['_data']['localId']).first()
        if not local_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="It seems like you've never explored the plantonic application before with this phone number.")

        otp_generated = utils.generate_new_otp()
        _, phone = utils.split_phone_number(username)
        is_otp_sent = False
        if otp_type == 'sms':
            is_otp_sent = otp_utils.send_sms_otp(otp_generated, phone)
        else:
            is_otp_sent = otp_utils.send_voice_otp(otp_generated, phone)
        
        if not is_otp_sent:
            raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="There are some problems sending OTP, please try again in some time.")

        new_otp = models.OTP(otp=str(otp_generated), username=username, customer_id=local_user.id, firebase_uid=local_user.firebase_uid, otp_type=otp_type)
        db.add(new_otp)
        db.commit()
        return {"status": True, "detail": "OTP has been sent successfully"}

    elif utils.is_email(username):
        user = firebase_auth.get_firebase_user_from_email(username)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="It seems like you don't have an account with this email.")

        local_user = db.query(models.User).filter(models.User.firebase_uid == user['_data']['localId']).first()
        if not local_user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="It seems like you've never explored the plantonic application before with this phone number.")

        otp_generated = utils.generate_new_otp()
        await otp_utils.send_email_otp(otp_generated, username, user['_data']['displayName'].split(' ')[0])

        new_otp = models.OTP(otp=str(otp_generated), username=username, customer_id=local_user.id, firebase_uid=local_user.firebase_uid, otp_type='email')
        db.add(new_otp)
        db.commit()
        return {"status": True, "detail": "OTP has been sent successfully"}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="You've entered an invalid username.")



@router.post("/verify_and_delete_user")
def verify_and_delete_user(verify_request: schemas.VerifyOTPRequestModel, db: Session = Depends(get_db)):
    existing_otp = db.query(models.OTP).filter(models.OTP.username == verify_request.username, models.OTP.created_at >= datetime.now() - timedelta(minutes=5)).order_by(models.OTP.created_at.desc()).first()
    print(existing_otp)
    if not existing_otp or existing_otp.is_used:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You've entered an invalid OTP.")

    if existing_otp.otp != str(verify_request.otp):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You've entered a wrong OTP.")
    # TODO
    # delete_account() 
    existing_otp.is_used = True
    db.commit()
    return {"status": True, "detail": "Your account and all related data has been deleted successfully"}
