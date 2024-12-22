from pydantic import BaseModel

class UserCreate(BaseModel):
    full_name: str
    city: str
    postal_code: str