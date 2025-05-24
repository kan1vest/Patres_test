from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from queries.orm import AsyncORM

from authx import AuthX, AuthXConfig

from schemas import BooksDeleteSсhema, BooksFilterSсhema, BooksUpdateSсhema, UserLoginSсhema, UserAuthSсhema, BooksSсhema

from config import settings

from passlib.context import CryptContext

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

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# Функция для проверки пароля
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

@router.post("/register/", tags=["Регистрация пользователей"])
async def register_user(creds: Annotated[UserLoginSсhema, Depends()]):
    existing_user = await AsyncORM.select_user(creds.email)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Пользователь c email {creds.email} уже существует")
    await AsyncORM.insert_users(creds.username, creds.email, creds.password) # добавляем в базу пользователя и хешируем пароль
    return {"msg": "Пользователь успешно зарегистрирован"}



@router.post("/auth", tags=["Авторизация"])
async def login(creds: Annotated[UserAuthSсhema, Depends()], response: Response):
    user = await AsyncORM.select_users_auth(creds.email)
    print(user)
    if user is None:
        raise HTTPException(status_code=401, detail=f"Имя пользователя не верно")
    verify = verify_password(creds.password, user[1])
    admin = verify_password(creds.password, get_password_hash(settings.ADMIN_psw))
    if admin:
        token = security_admin.create_access_token(creds.email, audience='Admin')
        response.set_cookie(config_admin.JWT_ACCESS_COOKIE_NAME, token)
        return {"msg": "Вы вошли в систему как администратор"}
    elif verify:
        token = security_user.create_access_token(creds.email, audience='User')
        response.set_cookie(config_user.JWT_ACCESS_COOKIE_NAME, token)
        return {"msg": "Вы вошли в систему как читатель"}
    else:
        raise HTTPException(status_code=401, detail=f"Пароль не верен")
    
@router.post("/protected_admin/book/create", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def create_books(task: Annotated[BooksSсhema, Depends()]):
   await AsyncORM.create_books(task.bookname, task.author, task.creat, task.ISBN, task.quantity)
   return {
    'msg': "Книга успешно добавлена",
    'Имя': task.bookname,
    'Автор': task.author,
    'Год создания': task.creat,
    'ISBN': task.ISBN,
    'Количество': task.quantity
   }


@router.get("/protected_admin/book/read", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def read_books(books_filter: Annotated[BooksFilterSсhema, Depends()], response: Response):
    res = await AsyncORM.select_books(books_filter)
    if res == []:
        return {
    'msg': "Книга не найдена",
    'Имя': books_filter.booknames, 
    'Автор':   books_filter.authors 
   }
    else:
        return res
    


@router.put("/protected_admin/book/", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def update_books(updates: Annotated[BooksUpdateSсhema, Depends()]):
    res = await AsyncORM.update_book(updates)
    return {'msg': f'Книга с параметрами {res[0]}, изменена на книгу с параметрами {res[1]}'}


@router.delete("/protected_admin/book/", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def delete_books(delete: Annotated[BooksDeleteSсhema, Depends()]):
    res = await AsyncORM.delete_book(delete)
    return {'msg': f'Книга с параметрами {res} успешно удалена'}
    


        