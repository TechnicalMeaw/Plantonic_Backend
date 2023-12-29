from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..instamojo import instamojo_payment as instamojo




router = APIRouter(prefix= "/payment/im",
                   tags=["Payment - Instamojo"])


@router.post("/new_order")
def create_new_order(db: Session = Depends(get_db)):
    instamojo.create_new_payment_request("1.00", "Santanu Mukherjee", "santanumukherjeebh@gmail.com", 8240251373)