import requests
from app.config import settings
from . import bd_utils as utils


def check_pin_code_availability(pincode: str):
    headers = {'Content-Type': 'application/json', "JWTToken": utils.generate_jwt_token()}
    payload = {
            "pinCode": pincode,
            "profile": {
                "Api_type": "S",
                "LicenceKey": settings.blue_dart_licence_key,
                "LoginID": settings.blue_dart_login_id
                }
            }
    
    res = requests.post('https://apigateway.bluedart.com/in/transportation/finder/v1/GetServicesforPincode', json=payload, headers=headers).json()

    print(res)
    try:
        if res['GetServicesforPincodeResult']['BharatDartCODInbound'] and res['GetServicesforPincodeResult']['BharatDartCODInbound'] == 'Yes' and res['GetServicesforPincodeResult']['BharatDartCODOutbound'] and res['GetServicesforPincodeResult']['BharatDartCODOutbound'] == 'Yes':
            return True
        else:
            return False
    except Exception:
        return False


def generate_waybill():
    pass