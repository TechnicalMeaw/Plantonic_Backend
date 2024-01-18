from fastapi import status, HTTPException, Depends, APIRouter
from .. import easyAes, models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session, load_only
from ..blue_dart import api as bd



router = APIRouter(prefix= "/profile",
                   tags=["Profile Page"])

@router.post("/feedback")
def post_feedback(feedback: schemas.FeedBackRequestModel ,db: Session = Depends(get_db), current_user : models.User = Depends(oauth2.get_current_user)):
    if not feedback.feedBack or feedback.feedBack == "":
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail= "Please write some feedback")

    feedback_item = models.Feedback(feedback=feedback.feedBack, customer_id = current_user.id)
    db.add(feedback_item)
    db.commit()
    
    return {"status": "Valid", "detail": "We received your valuable feedback."}