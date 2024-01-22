from datetime import datetime, timedelta
from typing import Optional
from fastapi import status, HTTPException, Depends, APIRouter
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from ..blue_dart import api as bd
from ..firebase import realtime_db
import math


router = APIRouter(prefix= "/deliver",
                   tags=["Delivery"])

@router.get("/check_pin_code", response_model = schemas.PinCodeAvailibility)
def check_pin_code(pincode: str, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    
    if not utils.is_valid_pin_code(pincode):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid pin code')

    if not bd.check_pin_code_availability(pincode):
        raise HTTPException(status_code=status.HTTP_405_METHOD_NOT_ALLOWED, detail='Delivery at this pin code is not available')
    
    return {"is_delivery_possible": True, "detail": ""}
   
        

@router.post("/place_order", response_model=schemas.PaceOrderResponseModel)
def place_order(all_orders: schemas.PlaceOrderRequestModel, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    try:
        for order in all_orders.all_orders:
            # product info
            product = realtime_db.get_product_info(order.productId)
            product_price = math.ceil(eval(product['actualPrice']))
            product_listed_price = product['listedPrice']

            # customer info
            customer_name = order.customerName
            customer_phone = order.phoneNo
            customer_email = order.email
            customer_address = order.address
            pincode = order.pincode

            # money
            quantity = order.quantity
            payable = product_price
            delivery_charge = eval(order.deliveryCharge)

            if delivery_charge > 0:
                payable += delivery_charge
            
            for _ in range(quantity):
                bd_response = bd.generate_waybill(full_address=customer_address, 
                                email= customer_email if customer_email is not None else "", 
                                phone_number= customer_phone,
                                name = customer_name,
                                pincode = pincode,
                                is_reverse_pickup = False,
                                product_name = product['productName'],
                                product_id = order.productId,
                                special_instruction = order.special_instructions,
                                product_count = 1, # Need special calculations
                                order_id= order.orderId,
                                pickup_date= utils.get_pickup_date(),
                                pickup_time= '1600',
                                breath= float(product['breadth']),
                                height= float(product['height']),
                                length= float(product['length']),
                                weight= product['weight'],
                                box_count= 1, # Default
                                amount_collectable= payable,
                                register_for_pickup= False # Need to change when production
                                )
                
                if not bd_response or not bd_response['GenerateWayBillResult'] or not bd_response['GenerateWayBillResult']['Status']:
                    continue

                bd_order = models.BlueDartOrders(bd_awb_no = bd_response['GenerateWayBillResult']['AWBNo'],
                                    bd_ccrcrdref = bd_response['GenerateWayBillResult']['CCRCRDREF'],
                                    bd_cluster_code = bd_response['GenerateWayBillResult']['ClusterCode'],
                                    bd_destination_area = bd_response['GenerateWayBillResult']['DestinationArea'],
                                    bd_destination_location = bd_response['GenerateWayBillResult']['DestinationLocation'],
                                    bd_is_error = bd_response['GenerateWayBillResult']['IsError'],
                                    bd_token_number = bd_response['GenerateWayBillResult']['TokenNumber'],
                                    bd_status_information = bd_response['GenerateWayBillResult']['Status'][0]['StatusInformation']
                                    )
                db.add(bd_order)
                db.commit()
                db.refresh(bd_order)

                if bd_response['GenerateWayBillResult']['IsError']:
                    continue

                new_order = models.Orders(customer_id= current_user.id,
                            product_id= order.productId,
                            merchant_id= order.merchantId,
                            customer_name= customer_name,
                            customer_full_address= customer_address,
                            customer_pincode= pincode,
                            customer_address_type= order.addressType,
                            customer_phone_number= customer_phone,
                            customer_payment_method= order.paymentMethod,
                            actual_order_quantity= quantity,
                            related_to_order_id= order.orderId,
                            transaction_id= order.transactionId,
                            payable= payable,
                            delivery_charge = delivery_charge,
                            product_listed_price= product_listed_price,
                            bd_order_id= bd_order.bd_awb_no,
                            special_instructions= order.special_instructions
                            )
                
                db.add(new_order)
                db.commit()

            # Delete product from cart
            realtime_db.delete_product_from_cart(user_id=current_user.firebase_uid, product_id=order.productId)

    except Exception:
        raise HTTPException(status_code=status.HTTP_424_FAILED_DEPENDENCY, detail="Something went wrong, some of the orders may not have been placed.")
    return {"status": "Valid", "detail": "Order placed successfully"}


@router.get("/orders")
def get_all_orders(page : int = 1, search: Optional[str] = "", is_admin: Optional[bool] = False, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):

    order_count = 0
    if is_admin:
        if current_user.role == 2:
            order_count = db.query(models.Orders).filter(models.Orders.merchant_id == current_user.firebase_uid).count()
        elif current_user.role == 3:
            order_count = db.query(models.Orders).count()
    else:
        order_count = db.query(models.Orders).filter(models.Orders.customer_id == current_user.id).count()

    if order_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No recent orders found")

    all_orders = None
    if is_admin:
        if current_user.role == 2:
            all_orders = db.query(models.Orders).filter(models.Orders.merchant_id == current_user.firebase_uid).order_by(models.Orders.order_id.desc()).limit(10).offset((page-1)*10).all()
        elif current_user.role == 3:
            all_orders = db.query(models.Orders).order_by(models.Orders.order_id.desc()).limit(10).offset((page-1)*10).all()
    else:
        all_orders = db.query(models.Orders).filter(models.Orders.customer_id == current_user.id).order_by(models.Orders.order_id.desc()).limit(10).offset((page-1)*10).all()

    if not all_orders:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "No more orders found")
            
    total_page = math.ceil(order_count/10)

    return {
            "data": all_orders, 
            "current_page": page, 
            "total_count": order_count,
            "total_page": total_page,
            "prev_page": page-1 if page > 1 else None, 
            "next_page": page+1 if page < total_page else None
            }


@router.post("/track_order", response_model=schemas.TrackOrderResponseModel)
def place_order(track_order: schemas.TrackOrderRequestModel, db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    order = db.query(models.Orders).filter(models.Orders.order_id == track_order.order_id, models.Orders.customer_id == current_user.id).first()
    if not order:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= "The order you're looking for is not found")
    res = bd.track_shipment(str(order.bd_order_id), order)
    return res