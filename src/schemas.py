
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLoginSсhema(BaseModel):
   username: str = Field('Nik')
   email: EmailStr = Field('Nik@yan.ru', pattern=r".+@*\.ru$")
   password: str = Field('11111')

class UserAuthSсhema(BaseModel):
   email: EmailStr = Field('Nik@yan.ru', pattern=r".+@*\.ru$")
   password: Optional[str] = Field('ADMIN')



class BooksSсhema(BaseModel):
   bookname: str = Field(pattern=r"^\S*$")
   author: str = Field(pattern=r"^\S*$")
   creat: str
   ISBN: str
   quantity: int


class BooksFilterSсhema(BaseModel):
    booknames: Optional[str] = Field('book_1,book_2', pattern=r"^\S*$")
    authors: Optional[str] = Field('author_1,author_2', pattern=r"^\S*$")
    
class BooksUpdateSсhema(BaseModel):
   bookname: Optional[str] = Field(pattern=r"^\S*$")
   bookname_new: Optional[str] = Field(None, pattern=r"^\S*$")
   author: Optional[str] = Field(None, pattern=r"^\S*$")
   author_new: Optional[str] = Field(None, pattern=r"^\S*$")
   creat: Optional[str] = Field(None)
   creat_new: Optional[str] = Field(None)
   ISBN: Optional[str] = Field(None)
   ISBN_new: Optional[str] = Field(None)
   quantity: Optional[int] = Field(None)
   quantity_new: Optional[int] = Field(None)

class BooksDeleteSсhema(BaseModel):
   bookname: Optional[str] = Field('book_1', pattern=r"^\S*$")