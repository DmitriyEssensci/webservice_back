from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from users_list.database import SessionLocal, Base, engine
from users_list.models import User
from users_list.schemas import UserCreate

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/users", tags=["users_list"])

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
        new_user = User(
            full_name=user.full_name, 
            city=user.city, 
            postal_code=user.postal_code,
        )
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {
            "message": "User added successfully", 
            "user": {
                "id": new_user.id, 
                "full_name": new_user.full_name
            }
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Удаление пользователя
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    return {"message": "Пользователь удален"}

# Редактирование пользователя
@router.put("/edit/{user_id}")
def edit_ads_object(
    user_id: int, updated_object: UserCreate, db: Session = Depends(get_db)
):
    ads_object = db.query(User).filter(User.id == user_id).first()
    if ads_object is None:
        raise HTTPException(status_code=404, detail="Объект не найден")

    # Редактируем только разрешённые поля
    if updated_object.full_name is not None:
        ads_object.full_name = updated_object.full_name
    if updated_object.city is not None:
        ads_object.city = updated_object.city
    if updated_object.postal_code is not None:
        ads_object.postal_code = updated_object.postal_code

    # Поле update_data обновится автоматически благодаря SQLAlchemy
    db.commit()
    db.refresh(ads_object)

    return {"message": "Объект обновлён", "object": ads_object}