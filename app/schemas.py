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
    role: str

# For token verification
class TokenData(BaseModel):
    id : Optional[str] = None

# For Pin Code
class PinCodeAvailibility(BaseModel):
    is_delivery_possible: bool
    detail: str
    class Config:
        from_attributes = True

# # For Banners
# class HomePageBannerObject(BaseModel):
#     image_link: str
#     index: int
#     created_at : str
#     id : int

#     class Config:
#         orm_mode = True


# class HomePageBannersResponseModel(BaseModel):
#     data: List[HomePageBannerObject]
#     detail: str