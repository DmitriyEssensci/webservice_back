# auth/login/routes.py
from fastapi import APIRouter

router = APIRouter(prefix="/", tags=["default"])

@router.get("/")
async def root():
    return {"message": "Hello World"}