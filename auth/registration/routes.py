from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta
from .models import RegUser
from .schemas import AuthUserCreate, Token
from .database import SessionLocal, engine, Base

# Инициализация криптографического контекста для хеширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT конфигурация
SECRET_KEY = "your_secret_key"  # Используйте безопасный ключ
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(prefix="/auth", tags=["auth"])

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Хеширование пароля
def hash_password(password: str) -> str:
    return pwd_context.hash(password)

# Регистрация нового пользователя
@router.post("/register", response_model=Token)
def register_user(user: AuthUserCreate, db: Session = Depends(get_db)):
    # Проверка, существует ли уже пользователь с таким логином
    db_user = db.query(RegUser).filter(RegUser.login == user.login).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким логином уже существует")

    # Хешируем пароль перед сохранением
    hashed_password = hash_password(user.password)

    # Создание нового пользователя
    new_user = RegUser(
        user_name=user.user_name,
        login=user.login,
        password=hashed_password,  # Сохраняем хешированный пароль
        mail=user.mail,
        phone_number=user.phone_number,
        secret_question=user.secret_question,
        secret_answer=user.secret_answer,
    )

    # Добавляем нового пользователя в базу данных
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Создаем JWT токен для нового пользователя
    access_token = create_access_token(data={"sub": new_user.login})

    return {"access_token": access_token, "token_type": "bearer", "user_name": new_user.user_name}

# Создание токена (для авторизации)
def create_access_token(data: dict, expires_delta: timedelta = None):  # Исправили аннотацию типа
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)