from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from sqlalchemy.orm import Session
from database import engine, SessionLocal, Base
from models import User, UserCreate
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    
@app.get("/users/")
def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return {"users": users}

@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    db.delete(user)
    db.commit()
    
    return {"message": "Пользователь удален"}