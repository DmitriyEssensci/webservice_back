from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from users_list.database import SessionLocal, Base
from users_list.models import User
from users_list.schemas import UserCreate

router = APIRouter(prefix="/users/api", tags=["users_list"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}