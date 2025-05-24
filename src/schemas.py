
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLoginSсhema(BaseModel):
   username: str 
   email: EmailStr = Field(pattern=r".+@*\.ru$")
   password: str = Field('11111')

class UserAuthSсhema(BaseModel):
   email: EmailStr = Field('Nik@yan.ru', pattern=r".+@*\.ru$")
   password: Optional[str] = Field('ADMIN')



