from fastapi import status, HTTPException, Depends, APIRouter
from datetime import datetime, timedelta
from app.otp_util import generateOtp, sendOTP
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..firebase import firebase_auth


router = APIRouter(prefix= "/auth",
                   tags=["Authentication"])
                   

@router.post("/", response_model = schemas.Token)
def get_user_token(user : schemas.GetAuthToken, db: Session = Depends(get_db)):
    aes = easyAes.EasyAES()
    # print(user.uid)
    user.uid = aes.decrypt(user.uid)

    print(user.uid)
    local_user = db.query(models.User).filter(user.uid == models.User.firebase_uid).first()

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
            return {"access_token": access_token, "token_type": "bearer"}
    else:
        # update last login
        local_user.last_login = datetime.now()
        db.commit()
        
        # create a token
        access_token = oauth2.create_access_token(data=local_user.id)
        return {"access_token": access_token, "token_type": "bearer"}
