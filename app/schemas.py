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
    
class LocationInfoResModel(BaseModel):
    region: str
    name: str
    dist: str
    state: str
    country: str
    pin: str

class PinCodeAvailibility(BaseModel):
    is_delivery_possible: bool
    detail: str
    # location_data: List[LocationInfoResModel]
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
        

class OrderItem(BaseModel):
    orderId: str
    merchantId : str 
    productId : str
    customerId: str
    customerName: str 
    address: str
    pincode: str
    addressType : str
    phoneNo: str 
    email : str
    paymentMethod: str
    quantity: int
    status: str
    transactionId: str
    timeStamp: int
    payable : str 
    listedPrice: str
    deliveryCharge: str
    deliveryDate: int
    special_instructions: str

class PlaceOrderRequestModel(BaseModel):
    all_orders: List[OrderItem]

class PaceOrderResponseModel(BaseModel):
    status: str 
    detail: str


class TrackOrderRequestModel(BaseModel):
    order_id: int


class Scan(BaseModel):
    Scan: str
    ScanCode: str
    ScanType: str    
    ScanDate: str
    ScanTime: str
    ScannedLocation: str
                  
class ScansItem(BaseModel):
    ScanDetail : List[Scan]

class ShipmentItem(BaseModel):
    Scans: ScansItem
    WaybillNo: str
    Origin: str
    Destination: str
    Status: str
    StatusType: str
    StatusDate: str
    StatusTime: str

class ShipmentDataItem(BaseModel):
    Shipment: ShipmentItem

class TrackOrderResponseModel(BaseModel):
    ShipmentData: ShipmentDataItem

 

#  Feedback
class FeedBackRequestModel(BaseModel):
    feedBack : str
    rating: Optional[str] = None