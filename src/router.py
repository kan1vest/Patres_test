from fastapi import APIRouter, Depends, HTTPException, Response
from typing import Annotated

from queries.orm import AsyncORM

from authx import AuthX, AuthXConfig, TokenPayload

import schemas

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
async def register_user(creds: Annotated[schemas.UserLoginSсhema, Depends()]):
    existing_user = await AsyncORM.select_user(creds.email)
    if existing_user:
        raise HTTPException(status_code=400, detail=f"Пользователь c email {creds.email} уже существует")
    await AsyncORM.insert_users(creds.username, creds.email, creds.password) # добавляем в базу пользователя и хешируем пароль
    return {"msg": "Пользователь успешно зарегистрирован"}



@router.post("/auth", tags=["Авторизация"])
async def login(creds: Annotated[schemas.UserAuthSсhema, Depends()], response: Response):
    user = await AsyncORM.select_users_auth(creds.email)
    if user is None:
        raise HTTPException(status_code=401, detail=f"Имя пользователя не верно")
    verify = verify_password(creds.password, user[1])
    admin = verify_password(creds.password, get_password_hash(settings.ADMIN_psw))
    if admin:
        token = security_admin.create_access_token(uid = str(user[2]), audience='Admin')
        response.set_cookie(config_admin.JWT_ACCESS_COOKIE_NAME, token)
        return {"msg": "Вы вошли в систему как администратор"}
    elif verify:
        token = security_user.create_access_token(uid = str(user[2]), audience='User')
        response.set_cookie(config_user.JWT_ACCESS_COOKIE_NAME, token)
        return {"msg": "Вы вошли в систему как читатель"}
    else:
        raise HTTPException(status_code=401, detail=f"Пароль не верен")
    




@router.post("/protected_admin/book/create", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def create_books(task: Annotated[schemas.BooksSсhema, Depends()]):
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
async def read_books(books_filter: Annotated[schemas.BooksFilterSсhema, Depends()], response: Response):
    res = await AsyncORM.select_books(books_filter)
    if res == []:
        return {
    'msg': "Книга не найдена",
    'Имя': books_filter.booknames, 
    'Автор':   books_filter.authors 
   }
    else:
        return res
    


@router.put("/protected_admin/book/update", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def update_books(updates: Annotated[schemas.BooksUpdateSсhema, Depends()]):
    res = await AsyncORM.update_book(updates)
    return {'msg': f'Книга с параметрами {res[0]}, изменена на книгу с параметрами {res[1]}'}


@router.delete("/protected_admin/book/delete", tags=["CRUD для книг"], dependencies=[Depends(security_admin.access_token_required)])
async def delete_books(delete: Annotated[schemas.BooksDeleteSсhema, Depends()]):
    res = await AsyncORM.delete_book(delete)
    return {'msg': f'Книга с параметрами {res} успешно удалена'}






@router.post("/protected_admin/user/create", tags=["CRUD для пользователей"], dependencies=[Depends(security_admin.access_token_required)])
async def create_user(task: Annotated[schemas.UserSсhema, Depends()]):
   await AsyncORM.create_user(task.username, task.email, task.password)
   return {'msg': f'Автор с параметрами {task.username, task.email, task.password} успешно добавлен'}



@router.get("/protected_admin/user/read", tags=["CRUD для пользователей"], dependencies=[Depends(security_admin.access_token_required)])
async def read_user(filter: Annotated[schemas.UserFilterSсhema, Depends()]):
    res = await AsyncORM.select_user(filter.email)
    if res == []:
        return {
    'msg': "Пользователь не найден",
    'Имя': filter.email
   }
    else:
        return {'Имя': res.username, 'email': res.email}
    

@router.put("/protected_admin/user/update", tags=["CRUD для пользователей"], dependencies=[Depends(security_admin.access_token_required)])
async def update_author(updates: Annotated[schemas.UserUpdateSсhema, Depends()]):
    res = await AsyncORM.update_user(updates)
    return {'msg': f'Пользователь с параметрами {res[0]}, изменен на пользователя с параметрами {res[1]}'}


@router.delete("/protected_admin/user/delete", tags=["CRUD для пользователей"], dependencies=[Depends(security_admin.access_token_required)])
async def delete_author(delete_data: Annotated[schemas.UserDeleteSсhema, Depends()]):
    res = await AsyncORM.delete_user(delete_data)
    return res

@router.get("/protected_user/user/get_book", tags=["Выдача книг"], dependencies=[Depends(security_user.access_token_required)])
async def get_book(books_filter: Annotated[schemas.BookFilterSсhema, Depends()], payload: TokenPayload = Depends(security_user.access_token_required)):
    res = await AsyncORM.get_book(books_filter.bookname, reader_id = int(payload.sub))    
    if res == None:
        return {
    'msg': f"К сожелению книги {books_filter.bookname} закончились, выберете другую",
   }
    elif res == 'Flag':
        return {
    'msg': "К сожелению у Вас 3 и более книг на руках, верните одну из них"
        }
    else:
        return f"{res['bookname']} успешно выдана читателю, остаток {res['quantity']} книг"
    

@router.get("/protected_user/user/return_book", tags=["Возват книг"], dependencies=[Depends(security_user.access_token_required)])
async def get_book(books_filter: Annotated[schemas.BookFilterSсhema, Depends()], payload: TokenPayload = Depends(security_user.access_token_required)):
    res = await AsyncORM.return_book(books_filter.bookname, reader_id = int(payload.sub))    
    if res == None:
        return {
    'msg': f"Книги с названием {books_filter.bookname} у Вас нет, возможно вы уже вернули их или ошиблись в названии",
   }
    else:
        return f"{res['bookname']} успешно возвращена, остаток {res['quantity']} книг"
    

@router.get("/protected_user/user/list_books", tags=["Список книг"], dependencies=[Depends(security_user.access_token_required)])
async def get_book():
    return await AsyncORM.list_books()
        

@router.get("/protected_user/user/list_book_of_reader", tags=["Список книг читателя"], dependencies=[Depends(security_user.access_token_required)])
async def get_book(payload: TokenPayload = Depends(security_user.access_token_required)):
    res = await AsyncORM.list_books_of_reader(reader_id = int(payload.sub))    
    if res == None:
        return {
    'msg': "У Вас нет книг",
   }
    else:
        return res
        

    


        