# auth/login/routes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .models import AuthUser
from .schemas import AuthUserLogin, Token
from .database import SessionLocal
from typing import Optional

router = APIRouter(prefix="/auth/api", tags=["auth"])

# Функция для получения сессии с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получение списка пользователей
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(AuthUserLogin).all()
    return {"users": users}