import time
from ..config import settings
import requests
import json
from .. import utils
from paytmchecksum import PaytmChecksum

# import checksum generation utility
# You can get this utility from https://developer.paytm.com/docs/checksum/


def new_order(userId: str, amount: int):

    order_id = "ORDERID_PAY_" + utils.current_milli_time()
    paytmParams = dict()

    paytmParams["body"] = {
        "requestType"   : "Payment",
        "mid"           : settings.paytm_merchant_id,
        "websiteName"   : "WEBSTAGING",
        "orderId"       : order_id,
        "callbackUrl"   : "https://plantonic.co.in/",
        "txnAmount"     : {
            "value"         : f"{amount}.00",
            "currency"      : "INR",
        },
        "userInfo" : {
        "custId" : userId,
        },
    }

    # Generate checksum by parameters we have in body
    # Find your Merchant Key in your Paytm Dashboard at https://dashboard.paytm.com/next/apikeys 
    checksum = PaytmChecksum.generateSignature(json.dumps(paytmParams["body"]), settings.paytm_merchant_id)

    paytmParams["head"] = {
        "channelId": "WAP",
        "signature": checksum
    }

    post_data = json.dumps(paytmParams)

    # for Staging
    url = f"https://securegw-stage.paytm.in/theia/api/v1/initiateTransaction?mid={settings.paytm_merchant_id}&orderId={order_id}"

    # for Production
    # url = "https://securegw.paytm.in/theia/api/v1/initiateTransaction?mid=YOUR_MID_HERE&orderId=ORDERID_98765"
    response = requests.post(url, data = post_data, headers = {"Content-type": "application/json"}).json()
    print(response)

    return response