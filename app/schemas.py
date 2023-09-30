from typing import List
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Get User Token Request Model
class GetAuthToken(BaseModel):
    uid : str

# Token response model
class Token(BaseModel):
    access_token : str
    token_type : str

# For token verification
class TokenData(BaseModel):
    id : Optional[str] = None

