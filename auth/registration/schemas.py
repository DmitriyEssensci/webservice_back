from pydantic import BaseModel, EmailStr

class AuthUserCreate(BaseModel):
    user_name: str
    login: str
    password: str
    mail: EmailStr
    phone_number: str
    secret_question: str
    secret_answer: str

class Token(BaseModel):
    access_token: str
    token_type: str
    user_name: str