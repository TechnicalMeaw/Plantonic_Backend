import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth

__cred = credentials.Certificate("./venv/serviceAccountKey.json")
firebase_admin.initialize_app(__cred)



def get_firebase_user(uid : str):
    try:
        user = auth.get_user(uid)        
        return user.__dict__
    except:
        return None

# user = get_firebase_user("PGWjTRhjDvOUe6iXfYOX3Q9xUdf2")
# print(user["_data"]["localId"])