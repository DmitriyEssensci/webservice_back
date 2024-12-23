from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import SessionLocal, Base, engine
from .models import AdsModel
from .schemas import AdsObject, AdsObjectUpdate

Base.metadata.create_all(bind=engine)

router = APIRouter(prefix="/ads", tags=["ads"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание объекта
@router.post("/")
def create_ads_object(object: AdsObject, db: Session = Depends(get_db)):
    try:
        new_ads_object = AdsModel(
            object_name=object.object_name,
            short_descr=object.short_descr,
            full_descr=object.full_descr,
            create_data=object.create_data,
        )
        db.add(new_ads_object)
        db.commit()
        db.refresh(new_ads_object)
        return {
            "message": "Ads object added successfully",
            "object": {
                "id": new_ads_object.id,
                "full_name": new_ads_object.object_name,
                "short_descr": new_ads_object.short_descr,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))

# Удаление объекта
@router.delete("/{ads_object_id}")
def delete_ads_object(ads_object_id: int, db: Session = Depends(get_db)):
    ads_object = db.query(AdsModel).filter(AdsModel.id == ads_object_id).first()
    if ads_object is None:
        raise HTTPException(status_code=404, detail="Объект не найден")
    db.delete(ads_object)
    db.commit()
    return {"message": "Объект удален"}

# Редактирование объекта
@router.put("/edit/{ads_object_id}")
def edit_ads_object(
    ads_object_id: int, updated_object: AdsObjectUpdate, db: Session = Depends(get_db)
):
    ads_object = db.query(AdsModel).filter(AdsModel.id == ads_object_id).first()
    if ads_object is None:
        raise HTTPException(status_code=404, detail="Объект не найден")

    # Редактируем только разрешённые поля
    if updated_object.object_name is not None:
        ads_object.object_name = updated_object.object_name
    if updated_object.short_descr is not None:
        ads_object.short_descr = updated_object.short_descr
    if updated_object.full_descr is not None:
        ads_object.full_descr = updated_object.full_descr

    # Поле update_data обновится автоматически благодаря SQLAlchemy
    db.commit()
    db.refresh(ads_object)

    return {"message": "Объект обновлён", "object": ads_object}