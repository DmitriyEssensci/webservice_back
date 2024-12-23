from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from contact.database import SessionLocal
from contact.models import Request

router = APIRouter(prefix="/contact/api", tags=["contact"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_requests(db: Session = Depends(get_db)):
    requests = db.query(Request).all()
    return {"requests": requests}