from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base
from .models import AdsModel
from .schemas import AdsObject

router = APIRouter(prefix="/ads/api", tags=["ads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(AdsModel).all()
    return {"objects": users}