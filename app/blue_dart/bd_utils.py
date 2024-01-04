import requests
from app.config import settings


def generate_jwt_token():
    payload = {'ClientID': settings.blue_dart_client_id, 'clientSecret': settings.blue_dart_client_secret}
    res = requests.get("https://apigateway.bluedart.com/in/transportation/token/v1/login", params=payload)

    return res.json()['JWTToken']

    