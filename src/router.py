from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

from queries.orm import AsyncORM

from schemas import UserLoginSсhema

router = APIRouter()


@router.post("/register/", tags=["Регистрация пользователей"])
async def register_user(creds: Annotated[UserLoginSсhema, Depends()]):
    existing_user = await AsyncORM.select_users_registration(creds.email, creds.password)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Пользователь уже существует")
    await AsyncORM.insert_users(creds.username, creds.email, creds.password) # добавляем в базу пользователя и хешируем пароль
    return {"msg": "Пользователь успешно зарегистрирован"}