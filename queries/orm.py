
from psycopg2 import IntegrityError
from sqlalchemy import and_, delete, or_, select, true
import sqlalchemy
from database import Base, async_engine, async_session_factory
from models import UsersOrm, BooksOrm


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Функция для хеширования пароля
def get_password_hash(password):
    return pwd_context.hash(password)


class AsyncORM:
    
    @staticmethod
    async def create_tables():
        async with async_engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
    
    @staticmethod
    async def insert_users(username_, email_, password_):
        async with async_session_factory() as session:
            user = UsersOrm(username = username_, email = email_, hashed_password = get_password_hash(password_))
            session.add_all([user])
            # flush взаимодействует с БД, поэтому пишем await
            await session.flush()
            await session.commit()


    @staticmethod
    async def select_user(email):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email)
                .filter_by(email = email)
            )
            res = await session.execute(query)
            result = res.first()
            return result
        
    @staticmethod
    async def select_users_auth(email):
        async with async_session_factory() as session:
            query = (
                select(UsersOrm.email, UsersOrm.hashed_password)
                .filter_by(email=email)
            )
            res = await session.execute(query)
            result = res.first()
            return result
        

    @staticmethod
    async def insert_books(): # для тестов потом удалить!!!!!!!!!!!!!!!!!!!!!!!!!!!
        async with async_session_factory() as session:
            book_1 = BooksOrm(bookname='book_1', author = 'author_1', creat='2025', ISBN='12123')
            book_2 = BooksOrm(bookname='book_2', author = 'author_2', creat='2024', ISBN='231242', quantity=2)
            book_3 = BooksOrm(bookname='book_3', author = 'author_3', creat='2021', ISBN='453454', quantity=3)
            book_4 = BooksOrm(bookname='book_4', author = 'author_4', creat='2023', ISBN='3545342',quantity=4)
            session.add_all([book_1, book_2, book_3, book_4])
            await session.flush() 
            await session.commit()

            

    @staticmethod
    async def create_books(bookname_, author_, creat_, ISBN_, quantity_):
        async with async_session_factory() as session:
            book = BooksOrm(bookname = bookname_, author = author_, creat = creat_, ISBN = ISBN_, quantity = quantity_)
            session.add(book)
            await session.flush() 
            await session.commit()


    @staticmethod
    async def select_books(books_filter):
        if books_filter.booknames:
            books = BooksOrm.bookname.in_(books_filter.booknames.split(','))
        else:
            books = true()
        if books_filter.authors:
            authors = BooksOrm.author.in_(books_filter.authors.split(','))
        else:
            authors = true()
        async with async_session_factory() as session:
            query = (
                select(BooksOrm)
                .where(
                    and_(
                        books, authors
                        )
                )
            )
            res = await session.execute(query)
            result = res.scalars().all()
            return result
        


    @staticmethod
    async def update_book(updates):
        async with async_session_factory() as session:
            query = (
                select(BooksOrm.id)
                .where(
                    BooksOrm.bookname.in_(updates.bookname.split(','))
                    )
            )
            res = await session.execute(query)
            upd_id = res.first() # получаем id для изменения данных в таблице
            upd = await session.get(BooksOrm, upd_id[0])
            print(upd)
            book = {
                'bookname': upd.bookname, 
                'author': upd.author, 
                'creat': upd.creat, 
                'ISBN': upd.ISBN, 
                'quantity': upd.quantity,
            }
            if updates.bookname_new:
                upd.bookname = updates.bookname_new
            if updates.author_new:
                upd.author = updates.author_new
            if updates.creat_new:
                upd.creat = updates.creat_new
            if updates.ISBN_new:
                upd.ISBN = updates.ISBN_new
            if updates.quantity_new:
                upd.quantity = updates.quantity_new
            book_update = {
                'bookname': upd.bookname, 
                'author': upd.author, 
                'creat': upd.creat, 
                'Genre': upd.ISBN, 
                'quantity': upd.quantity,
            }     
            await session.flush()
            await session.commit()
            return book, book_update
        



    @staticmethod
    async def delete_book(delete_data):
        async with async_session_factory() as session:
            query_select = (
                select(BooksOrm)
                .filter(
                    BooksOrm.bookname.contains(delete_data.bookname)
                )
                    )
            query_delete = (
                delete(BooksOrm)
                .filter(
                    BooksOrm.bookname.contains(delete_data.bookname),
                    )
            )
            res = await session.execute(query_select)
            await session.execute(query_delete)
            result = res.scalars().all()
            await session.commit()
            return result   
            