from sqlalchemy import Column, Integer, String
from .database import Base

class RegUser(Base):
    __tablename__ = 'reg'

    id = Column(Integer, primary_key=True, index=True)
    user_name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    login = Column(String, unique=True, index=True, nullable=False)
    mail = Column(String, unique=True, nullable=False)
    phone_number = Column(String, unique=True, nullable=False)
    secret_question = Column(String, nullable=False)
    secret_answer = Column(String, nullable=False)