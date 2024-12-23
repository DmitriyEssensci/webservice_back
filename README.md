# webservice_back
Барбисайз гёрл детка лезет в мой карман

# Закидывание пакетов pip
pip3 freeze > requirements.txt

# Установка с пакетов pip
pip3 install -r requirements.txt

## Роутинги
- /contact - contact
- / - default
- /users
- /ads
- /auth

### Подроуты и методы /contact - contact

### Подроуты и методы / - default
- /default - Hello World

### Подроуты и методы /users - users_list
POST - Create user
- /users
DELETE - Delete user
- /users/{user_id}
PUT - Edit user
- /users/edit/{user_id}
GET - Get users
- /users/api

### Подроуты и методы /ads - ads
POST - Create object
- /ads
DELETE - Delete object
- /ads/{ads_object_id}
PUT - Edit object
- /ads/edit/{ads_object_id}
GET - Get object
- /ads/api

### Подроуты и методы /auth - auth
#### /auth/login
**/auth/login**
POST - login in user
- /auth/login
GET - get users
- /auth/api

**/auth/registration**
POST - registration in user
- /auth/register

## Маршруты:
- /default - Hello World
- /users
- /users/{user_id}
- /users/edit/{user_id}
- /users/api
- /ads
- /ads/{ads_object_id}
- /ads/edit/{ads_object_id}
- /edit/api
- /auth/login
- /auth/api

## Окружение:
- Swager: http://127.0.0.1:8000/docs#/
- Backend: http://127.0.0.1:8000/
- СУБД - postgres: 
    - postgresql://postgres:postgres@localhost:5432/postgres
    - postgresql://postgres:postgres@localhost:5432/email