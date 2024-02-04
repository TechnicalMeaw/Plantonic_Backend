import requests
from app.config import settings
from . import bd_utils as utils
from app import utils as app_utils
import xmltodict
from .. import models


def check_pin_code_availability(pincode: str):
    headers = {'Content-Type': 'application/json', "JWTToken": utils.generate_jwt_token()}
    payload = {
            "pinCode": pincode,
            "profile": {
                "Api_type": settings.blue_dart_api_type,
                "LicenceKey": settings.blue_dart_licence_key,
                "LoginID": settings.blue_dart_login_id
                }
            }
    
    res = requests.post('https://apigateway.bluedart.com/in/transportation/finder/v1/GetServicesforPincode', json=payload, headers=headers).json()

    try:
        if res['GetServicesforPincodeResult']['BharatDartCODInbound'] and res['GetServicesforPincodeResult']['BharatDartCODInbound'] == 'Yes' and res['GetServicesforPincodeResult']['BharatDartCODOutbound'] and res['GetServicesforPincodeResult']['BharatDartCODOutbound'] == 'Yes':
            return True
        else:
            return False
    except Exception:
        return False


def generate_waybill(full_address: str, email: str, phone_number: str, name: str, pincode: str, weight: str, amount_collectable: int,\
                      box_count: int, is_reverse_pickup: bool, breath: float, height: float, length: float, order_id: str, register_for_pickup: bool,\
                        special_instruction: str, pickup_time: str, pickup_date: str, product_id: str, product_name: str, product_count: int):
    payload = {
        "Request":{
            "Consignee":{
                "AvailableDays":"",
                "AvailableTiming":"",
                "ConsigneeAddress1": full_address,
                "ConsigneeAddress2":"",
                "ConsigneeAddress3":"",
                "ConsigneeAddressType":"",
                "ConsigneeAddressinfo":"",
                "ConsigneeAttention":"",
                "ConsigneeEmailID": email if email is not None else "",
                "ConsigneeFullAddress": full_address,
                "ConsigneeGSTNumber":"",
                "ConsigneeLatitude":"",
                "ConsigneeLongitude":"",
                "ConsigneeMaskedContactNumber":"",
                "ConsigneeMobile": phone_number,
                "ConsigneeName": name,
                "ConsigneePincode": pincode,
                "ConsigneeTelephone":""
            },
            "Returnadds":{
                "ManifestNumber":"",
                "ReturnAddress1": settings.merchant_address,
                "ReturnAddress2":"",
                "ReturnAddress3":"",
                "ReturnAddressinfo":"",
                "ReturnContact":"Plantonic Business & Co.",
                "ReturnEmailID": settings.mail_id,
                "ReturnLatitude":"",
                "ReturnLongitude":"",
                "ReturnMaskedContactNumber":"",
                "ReturnMobile": settings.merchant_phone_number,
                "ReturnPincode": settings.merchant_pincode,
                "ReturnTelephone":""
            },
            "Services":{
                "AWBNo":"",
                "ActualWeight": weight,
                "CollectableAmount": amount_collectable,
                "Commodity":{
                    "CommodityDetail1":"",
                    "CommodityDetail2":"",
                    "CommodityDetail3":""
                },
                "CreditReferenceNo": str(app_utils.current_milli_time()),       
                "CreditReferenceNo2":"",
                "CreditReferenceNo3":"",
                "DeclaredValue": amount_collectable,
                "DeliveryTimeSlot":"",
                "Dimensions":[
                    {
                    "Breadth": breath,
                    "Count": box_count if box_count is not None else 1,
                    "Height": height,
                    "Length": length
                    }
                ],
                "FavouringName":"",
                "IsDedicatedDeliveryNetwork": False,
                "IsDutyTaxPaidByShipper": False,
                "IsForcePickup": False,
                "IsPartialPickup": False,
                "IsReversePickup": is_reverse_pickup if is_reverse_pickup is not None else False,
                "ItemCount": product_count if product_count is not None else 1,
                "Officecutofftime":"",
                "PDFOutputNotRequired": False,
                "PackType":"",
                "ParcelShopCode":"",
                "PayableAt":"",
                "PickupDate": f"/Date({pickup_date})/",
                "PickupMode":"",
                "PickupTime": pickup_time,
                "PickupType":"",
                "PieceCount": str(box_count) if box_count is not None else "1",
                "PreferredPickupTimeSlot":"",
                "ProductCode":"A",
                "ProductFeature":"",
                "ProductType":1,
                "RegisterPickup": register_for_pickup if register_for_pickup is not None else False,
                "SpecialInstruction": special_instruction if special_instruction is not None else "",
                "SubProductCode":"C",
                "TotalCashPaytoCustomer":0,
                "itemdtl":[
                    {
                    "CGSTAmount":0,
                    "HSCode":"",
                    "IGSTAmount":0,
                    "Instruction": special_instruction if special_instruction is not None else "",
                    "InvoiceDate":f"/Date({app_utils.current_milli_time()})/",
                    "InvoiceNumber": order_id,
                    "ItemID":"",
                    "ItemName": product_name if product_name is not None else "Plant",
                    "ItemValue": amount_collectable,
                    "Itemquantity": product_count if product_count is not None else 1,
                    "PlaceofSupply":"",
                    "ProductDesc1": "plantonic.co.in",
                    "ProductDesc2": product_name if product_name is not None else "Plant",
                    "ReturnReason":"",
                    "SGSTAmount":0,
                    "SKUNumber":"",
                    "SellerGSTNNumber": settings.gst_number,
                    "SellerName":"Plantonic.co.in",
                    "SubProduct1":"",
                    "SubProduct2":"",
                    "TaxableAmount":0,
                    "TotalValue":amount_collectable,
                    "cessAmount":"0.0",
                    "countryOfOrigin":"IN",
                    "docType":"",
                    "subSupplyType":0,
                    "supplyType":""
                    }
                ],
                "noOfDCGiven":0
            },
            "Shipper":{
                "CustomerAddress1": settings.merchant_address,
                "CustomerAddress2":"",
                "CustomerAddress3":"",
                "CustomerAddressinfo":"",
                "CustomerBusinessPartyTypeCode":"",
                "CustomerCode": settings.blue_dart_customer_code,
                "CustomerEmailID": settings.mail_id,
                "CustomerGSTNumber":"",
                "CustomerLatitude":"",
                "CustomerLongitude":"",
                "CustomerMaskedContactNumber":"",
                "CustomerMobile": settings.merchant_phone_number,
                "CustomerName":"Plantonic",
                "CustomerPincode": settings.merchant_pincode,
                "CustomerTelephone":"",
                "IsToPayCustomer": False,
                "OriginArea": settings.blue_dart_area_code,
                "Sender":"Plantonic",
                "VendorCode":""
            }
        },
        "Profile":{
            "Api_type": settings.blue_dart_api_type,
            "LicenceKey": settings.blue_dart_licence_key,
            "LoginID": settings.blue_dart_login_id
        }
    }

    headers = {'Content-Type': 'application/json', "JWTToken": utils.generate_jwt_token()}
    
    res = requests.post('https://apigateway.bluedart.com/in/transportation/waybill/v1/GenerateWayBill', json=payload, headers=headers).json()

    return res



def is_shipment_delivered(awb_no : str):
    headers = {'Content-Type': 'application/json', "JWTToken": utils.generate_jwt_token()}

    res = requests.get(f'https://apigateway.bluedart.com/in/transportation/tracking/v1?handler=tnt&action=custawbquery&loginid={settings.blue_dart_login_id}&format=json&awb=awb&numbers={awb_no}&lickey={settings.blue_dart_tracking_licence_key}&verno=1.3&scan=1', headers=headers).json()
    
    try:
        return res['ShipmentData']['Shipment'][0]['StatusType'] == 'DL'
    except Exception:
        return False



def track_shipment(awb_no : str, order: models.Orders):
    headers = {'Content-Type': 'application/json', "JWTToken": utils.generate_jwt_token()}

    res = requests.get(f'https://apigateway.bluedart.com/in/transportation/tracking/v1?handler=tnt&action=custawbquery&loginid={settings.blue_dart_login_id}&awb=awb&numbers={awb_no}&lickey={settings.blue_dart_tracking_licence_key}&verno=1.3&scan=1', headers=headers)
        

    json_res = xmltodict.parse(res.text)
    temp=[]

    try:
        json_res["ShipmentData"]['Shipment']["WaybillNo"]= awb_no
        
        if type(json_res['ShipmentData']['Shipment']['Scans']['ScanDetail']) == dict:
            temp.append(json_res['ShipmentData']['Shipment']['Scans']['ScanDetail'])
            json_res['ShipmentData']['Shipment']['Scans']['ScanDetail'] = temp
    except Exception:
        json_res = {
                "ShipmentData":{
                    "Shipment":{
                        "WaybillNo": awb_no,
                        "Origin":"AMTALA BDEL",
                        "Destination":"AMTALA BDEL",
                        "Status":"Online shipment booked",
                        "StatusType":"PU",
                        "StatusDate": order.created_at.strftime("%d %B %Y"),
                        "StatusTime": order.created_at.strftime("%H:%M"),
                        "Scans":{
                            "ScanDetail":[
                            {
                                "Scan":"Online shipment booked",
                                "ScanCode":"030",
                                "ScanType":"PU",
                                "ScanGroupType":"S",
                                "ScanDate": order.created_at.strftime("%d %B %Y"),
                                "ScanTime": order.created_at.strftime("%H:%M"),
                                "ScannedLocation":"AMTALA BDEL",
                                "ScannedLocationCode":"AAM"
                            }
                            ]
                        }
                    }
                }
            }

    scans = json_res['ShipmentData']['Shipment']['Scans']['ScanDetail']
    
    json_res['ShipmentData']['Shipment']['Scans']['ScanDetail'] = sorted(scans, key = lambda x: (x['ScanDate'], x['ScanTime']))

    return json_res


# track_shipment('80401604146')