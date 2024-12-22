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

# Конфигурация для JWT
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Инициализация криптографического контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

router = APIRouter(prefix="/auth", tags=["auth"])

# Функция для получения сессии с БД
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Функция для создания JWT токена
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# Функция для проверки пароля
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

# Логика для входа пользователя
@router.post("/login", response_model=Token)
def login_user(user: AuthUserLogin, db: Session = Depends(get_db)):
    db_user = db.query(AuthUser).filter(AuthUser.login == user.login).first()

    # Если пользователь не найден или пароль неверный
    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")

    # Генерация токена
    access_token = create_access_token(data={"sub": db_user.login})
    return {"access_token": access_token, "token_type": "bearer", "user_name": db_user.user_name}