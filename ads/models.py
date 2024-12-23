from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from .database import Base

class AdsModel(Base):
    __tablename__ = "ads_objects"

    id = Column(Integer, primary_key=True, index=True)
    object_name = Column(String, nullable=False)
    short_descr = Column(String, nullable=False)
    full_descr = Column(String, nullable=False)
    create_data = Column(DateTime, default=datetime.utcnow, nullable=False)  # Автоматически задаётся при создании
    update_data = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)  # Автоматически обновляется