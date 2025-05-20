from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from queries.orm import AsyncORM

from schemas import UserLoginSсhema, UserAuthSсhema

router = APIRouter()


@router.post("/register/", tags=["Регистрация пользователей"])
async def register_user(creds: Annotated[UserLoginSсhema, Depends()]):
    existing_user = await AsyncORM.select_users_registration(creds.email)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Пользователь c email {creds.email} уже существует")
    await AsyncORM.insert_users(creds.username, creds.email) # добавляем в базу пользователя и хешируем пароль
    return {"msg": "Пользователь успешно зарегистрирован"}



""" 
@router.post("/login", tags=["Авторизация"])
async def login(creds: Annotated[UserAuthSсhema, Depends()], 
                response: Response):
    user = await AsyncORM.select_users_auth(creds.email, creds.password)
    verify = verify_password(creds.password, user[1])
    admin = verify_password(creds.password, get_password_hash(settings.ADMIN_psw))
    if admin:
        token = security_admin.create_access_token(creds.email, audience='Admin')
        response.set_cookie(config_admin.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    elif verify:
        token = security_user.create_access_token(creds.email, audience='User')
        response.set_cookie(config_user.JWT_ACCESS_COOKIE_NAME, token)
        return {"access_token": token}
    else: 
        raise HTTPException(status_code=401, detail="Не верный пароль") """