from sqlalchemy import (
    Column,
    Integer,
    String,
    text,
)


from database import Base





class UsersOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

class BooksOrm(Base):   # создаем таблицы
    __tablename__ = "books_table" 

    id = Column(Integer, primary_key=True, index=True)
    bookname = Column(String)
    author = Column(String)
    creat = Column(String)
    ISBN = Column(String, unique=True)
    quantity = Column(Integer, server_default=text("1"))
    

