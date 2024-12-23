from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
from datetime import datetime

class Request(Base):
    __tablename__ = "request"

    id = Column(Integer, primary_key=True, index=True)
    sender_name = Column(String, nullable=False)
    sender_email = Column(String, nullable=False)
    sender_number = Column(String, nullable=False)
    data = Column(String, nullable=False)
    create_data = Column(DateTime, default=datetime.utcnow, nullable=False)
    

