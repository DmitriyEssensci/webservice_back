from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .models import Request
from .schemas import RequestCreate

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/contact", tags=["contact"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание запроса
@router.post("/")
def create_request(request: RequestCreate, db: Session = Depends(get_db)):
    try:
        new_request = Request(
            sender_name=request.sender_name,
            sender_email=request.sender_email,
            sender_number=request.sender_number,
            data=request.data,
            create_data=request.create_data,
        )
        db.add(new_request)
        db.commit()
        db.refresh(new_request)
        return {
            "message": "Request added successfully", 
            "user": {
                "id": new_request.id, 
                "data": new_request.data,
                "sender_email": new_request.sender_email
            }
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Удаление запроса
@router.delete("/{request_id}")
def delete_reuest(request_id: int, db: Session = Depends(get_db)):
    request = db.query(Request).filter(Request.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Request not found")
    db.delete(request)
    db.commit()
    return {"message": "Request deleted successfully", "id": request_id}

# Редактирование запроса
@router.put("/edit/{request_id}")
def edit_request(
    request_id: int, updated_object: RequestCreate, db: Session = Depends(get_db)
):
    request = db.query(Request).filter(Request.id == request_id).first()
    if request is None:
        raise HTTPException(status_code=404, detail="Объект не найден")

    if updated_object.sender_name is not None:
        request.sender_name = updated_object.sender_name
    if updated_object.sender_email is not None:
        request.sender_email = updated_object.sender_email
    if updated_object.sender_number is not None:
        request.sender_number = updated_object.sender_number
    if updated_object.data is not None:
        request.data = updated_object.data
    if updated_object.create_data is not None:
        request.create_data = updated_object.create_data

    db.commit()
    db.refresh(request)

    return {"message": "Request successfull edited", "request": request}