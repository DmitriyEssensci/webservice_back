from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from default.routes import router as default

from users_list.routes import router as users_router
from users_list.api import router as users_router_api

from auth.registration.routes import router as auth_reg
from auth.login.routes import router as auth_login
from auth.login.api import router as auth_login_api

from ads.routes import router as ads_router
from ads.api import router as ads_router_api

from contact.routes import router as contact_router
from contact.api import router as contact_router_api

app = FastAPI()

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение маршрутов пользователей
app.include_router(default)

app.include_router(users_router)
app.include_router(users_router_api)

app.include_router(auth_reg)
app.include_router(auth_login)
app.include_router(auth_login_api)

app.include_router(ads_router)
app.include_router(ads_router_api)

app.include_router(contact_router)
app.include_router(contact_router_api)
