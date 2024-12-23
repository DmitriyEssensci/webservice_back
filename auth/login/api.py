# auth/login/routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .schemas import AuthUserLogin
from .database import SessionLocal

router = APIRouter(prefix="/auth/api", tags=["auth"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(AuthUserLogin).all()
    return {"users": users}