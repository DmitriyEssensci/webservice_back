from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from users_list.database import SessionLocal, Base
from users_list.models import User
from users_list.schemas import UserCreate

router = APIRouter(prefix="/users", tags=["users_list"])

# Функция для подключения к базе данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание пользователя
@router.post("/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(full_name=user.full_name, city=user.city, postal_code=user.postal_code)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User added successfully", "user": {"id": new_user.id, "full_name": new_user.full_name}}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Получение списка пользователей
@router.get("/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

# Удаление пользователя
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удален"}