from fastapi import status, HTTPException, Depends, APIRouter
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session, load_only
from ..blue_dart import api as bd



router = APIRouter(prefix= "/home",
                   tags=["Home Page"])

@router.get("/get_banners")
def get_all_banners(db: Session = Depends(get_db)):

    all_banners = db.query(models.HomePageBanners).all()
    return {"data": all_banners, "detail": ""}