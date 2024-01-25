from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import json
from app.config import settings

# Define the required scopes
scopes = [
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account
credentials = service_account.Credentials.from_service_account_file(
    "./venv/serviceAccountKey.json", scopes=scopes)

# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)



def get_product_info(product_id: str):
    response = authed_session.get(
    f"{settings.firebase_realtime_db_url}/products/{product_id}.json")

    return dict(json.loads(response.content.decode('utf-8')))


def delete_product_from_cart(user_id: str, product_id: str):
    authed_session.delete(f"{settings.firebase_realtime_db_url}/cart/{user_id}/{product_id}.json")

def update_product_quantity(product_id: str, quantity: int):
    current_quantity = authed_session.get(f"{settings.firebase_realtime_db_url}/products/{product_id}/currentStock.json")
    to_be_quantity = int(current_quantity.json()) - quantity
    if to_be_quantity < 0:
        to_be_quantity = 0
        # return int(0 - to_be_quantity)                                  
    res = authed_session.patch(f"{settings.firebase_realtime_db_url}/products/{product_id}.json", json={"currentStock": to_be_quantity})
    print(res.json())

# update_product_quantity('1a918ecc-8919-4a62-afd1-46798e0cfeca', 4)