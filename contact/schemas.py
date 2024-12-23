from pydantic import BaseModel
from .database import Base
from datetime import datetime

class RequestCreate(BaseModel):
    sender_name: str
    sender_email: str
    sender_number: str
    data: str
    create_data: datetime

    class Config:
        orm_mode = True