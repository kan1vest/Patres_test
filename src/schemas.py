
import email
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, field_validator


class UserLoginSсhema(BaseModel):
   username: str = Field('Nik')
   email: EmailStr = Field('Nik@yan.ru', pattern=r".+@*\.ru$")
   password: str = Field('11111')

class UserAuthSсhema(BaseModel):
   email: EmailStr = Field('Nik@yan.ru', pattern=r".+@*\.ru$")
   password: Optional[str] = Field('11111')



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


class UserSсhema(BaseModel):
   username: str
   email: EmailStr = Field(pattern=r".+@*\.ru$")
   password: str


class UserFilterSсhema(BaseModel):
   email: EmailStr = Field(pattern=r".+@*\.ru$")


class UserUpdateSсhema(BaseModel):
   username_new: Optional[str] = Field(None, pattern=r"^\S*$")
   email: EmailStr = Field(pattern=r".+@*\.ru$")
   email_new: EmailStr = Field(None, pattern=r".+@*\.ru$")
   password_new: Optional[str] = Field(None)

class UserDeleteSсhema(BaseModel):
   email: EmailStr = Field(pattern=r".+@*\.ru$")


class BookFilterSсhema(BaseModel):
   bookname: Optional[str] = Field('book_1', pattern=r"^\S*$")
   