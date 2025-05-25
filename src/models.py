import datetime
from typing import Annotated
from sqlalchemy import (
    Column,
    Integer,
    String,
    Time,
    text,
)


from database import Base

from sqlalchemy.orm import Mapped, mapped_column

borrow_date = Annotated[datetime.datetime, mapped_column(server_default=text("TIMEZONE('utc-3', now())"))]


class UsersOrm(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String)
    email = Column(String, unique=True)
    hashed_password = Column(String)

class BooksOrm(Base):   
    __tablename__ = "books_table" 

    id = Column(Integer, primary_key=True, index=True)
    bookname = Column(String)
    author = Column(String)
    creat = Column(String)
    ISBN = Column(String, unique=True)
    quantity = Column(Integer, server_default=text("1"))


class BorrowedBooksOrm(Base):
    __tablename__ = "Borrowed_Books" 

    id = Column(Integer, primary_key=True, index=True)
    book_id = Column(Integer)
    reader_id = Column(Integer)
    borrow_date: Mapped[borrow_date]
    return_date = Column(String, server_default = 'NULL')
    

