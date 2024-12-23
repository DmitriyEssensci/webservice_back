from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import AdsModel

router = APIRouter(prefix="/ads/api", tags=["ads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_ads_objects(db: Session = Depends(get_db)):
    ads_objects = db.query(AdsModel).all()
    return {"objects": ads_objects}