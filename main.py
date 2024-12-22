from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from .default.routes import router as default
from users_list.routes import router as users_router
from auth.registration.routes import router as auth_reg
from auth.login.routes import router as auth_login

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов пользователей
# app.include_router(default)
app.include_router(users_router)
app.include_router(auth_reg)
app.include_router(auth_login)

@app.get("/")
async def root():
    return {"message": "Hello World"}