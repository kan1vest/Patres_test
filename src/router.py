from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from queries.orm import AsyncORM

from authx import AuthX, AuthXConfig

from schemas import UserLoginSсhema, UserAuthSсhema

from config import settings

""" from passlib.context import CryptContext """

router = APIRouter()




config_user = AuthXConfig()
config_user.JWT_SECRET_KEY = settings.SECURITY_USER_JWT_secret_key
config_user.JWT_ACCESS_COOKIE_NAME = settings.SECURITY_USER_JWT_ACCESS_COOKIE_NAME
config_user.JWT_TOKEN_LOCATION = settings.SECURITY_USER_JWT_token_location
config_user.JWT_DECODE_AUDIENCE = settings.SECURITY_USER_JWT_decode_audience
config_user.JWT_COOKIE_CSRF_PROTECT = False

config_admin = AuthXConfig()
config_admin.JWT_SECRET_KEY = settings.SECURITY_ADMIN_JWT_secret_key
config_admin.JWT_ACCESS_COOKIE_NAME = settings.SECURITY_ADMIN_JWT_ACCESS_COOKIE_NAME
config_admin.JWT_TOKEN_LOCATION = settings.SECURITY_ADMIN_JWT_token_location
config_admin.JWT_DECODE_AUDIENCE = settings.SECURITY_ADMIN_JWT_decode_audience
config_admin.JWT_COOKIE_CSRF_PROTECT = False # РАЗОБРАТЬСЯ ИСПРАВИТЬ !!!

security_user = AuthX(config=config_user)
security_admin = AuthX(config=config_admin)

""" pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password) """

@router.post("/register/", tags=["Регистрация пользователей"])
async def register_user(creds: Annotated[UserLoginSсhema, Depends()]):
    existing_user = await AsyncORM.select_user(creds.email)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Пользователь c email {creds.email} уже существует")
    await AsyncORM.insert_users(creds.username, creds.email) # добавляем в базу пользователя и хешируем пароль
    return {"msg": "Пользователь успешно зарегистрирован"}



@router.post("/login", tags=["Авторизация"])
async def login(creds: Annotated[UserAuthSсhema, Depends()], response: Response):
    user = await AsyncORM.select_user(creds.email)
    if user is None:
        raise HTTPException(status_code=401, detail=f"Пользователь c email {creds.email} не существует")
    else:
        if creds.password == 'ADMIN':
            """ admin = verify_password(creds.password, get_password_hash(settings.ADMIN_psw)) """
            token = security_admin.create_access_token(creds.email, audience='Admin')
            response.set_cookie(config_admin.JWT_ACCESS_COOKIE_NAME, token)
            return {"msg": "Вы вошли в систему как администратор"}
        else:
            token = security_user.create_access_token(creds.email, audience='User')
            response.set_cookie(config_user.JWT_ACCESS_COOKIE_NAME, token)
            return {"msg": "Вы вошли в систему как читатель"}
        