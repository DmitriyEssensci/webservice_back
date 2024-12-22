# auth/login/schemas.py
from pydantic import BaseModel

class AuthUserLogin(BaseModel):
    login: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str

    class Config:
        orm_mode = True