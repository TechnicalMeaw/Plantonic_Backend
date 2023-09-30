from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
import json

# Define the required scopes
scopes = [
  "https://www.googleapis.com/auth/userinfo.email",
  "https://www.googleapis.com/auth/firebase.database"
]

# Authenticate a credential with the service account
credentials = service_account.Credentials.from_service_account_file(
    "key/serviceAccountKey.json", scopes=scopes)

# Use the credentials object to authenticate a Requests session.
authed_session = AuthorizedSession(credentials)
response = authed_session.get(
    "https://plantonic-cc6d5-default-rtdb.asia-southeast1.firebasedatabase.app/products.json")

d = dict(json.loads(response.content.decode('utf-8')))

for key, value in d.items():
    print(key, value)
