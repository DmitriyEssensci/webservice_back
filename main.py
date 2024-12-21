from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import User, UserCreate
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError
from fastapi import HTTPException

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Разрешённый адрес фронтенда
    allow_methods=["*"],
    allow_headers=["*"],
)

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def root():
    return {"message": "Hello World"}

Base.metadata.create_all(bind=engine)

# POST-запрос для добавления нового пользователя 
@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        new_user = User(full_name=user.full_name, city=user.city, postal_code=user.postal_code)
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return {"message": "User added successfully", "user": {"id": new_user.id, "full_name": new_user.full_name}}
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))