from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class AdsObject(BaseModel):
    object_name: str
    short_descr: str
    full_descr: str
    create_data: datetime
    update_data: datetime

    class Config:
        orm_mode = True

class AdsObjectUpdate(BaseModel):
    object_name: Optional[str] = None
    short_descr: Optional[str] = None
    full_descr: Optional[str] = None

    class Config:
        orm_mode = True