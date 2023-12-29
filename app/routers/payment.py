from fastapi import status, HTTPException, Depends, APIRouter
from datetime import datetime, timedelta
from app.otp_util import generateOtp, sendOTP
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..firebase import firebase_auth
from ..paytm import paytm_payment

import time
from ..config import settings
import requests
import json
from .. import utils
from paytmchecksum import PaytmChecksum



router = APIRouter(prefix= "/payment/tm",
                   tags=["Payment - PayTM"])


@router.get("/new_order")
def create_new_order(db: Session = Depends(get_db)):

    order_id = "ORDERID_PAY_" + str(utils.current_milli_time())
    paytmParams = dict()

    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : str(settings.paytm_key),
        "websiteName"   : "WEBSTAGING",
        "orderId"       : str(order_id),
        "callbackUrl"   : "https://plantonic.co.in/",
        "txnAmount"     : {
            "value"         : "1.00",
            "currency"      : "INR",
        },
        "userInfo" : {
        "custId" : "fjytfjyh",
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), str(settings.paytm_key))

    paytmParams["head"] = {
        "channelId": "WAP",
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={settings.paytm_key}&orderId={order_id}"

    # for Production
    # url = f"https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid={settings.paytm_merchant_id}&orderId={order_id}"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)

    return response
