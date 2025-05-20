
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class UserLoginSсhema(BaseModel):
   username: str 
   email: EmailStr = Field(pattern=r".+@*\.ru$")

class UserAuthSсhema(BaseModel):
   email: EmailStr = Field('Nik@example.com', pattern=r".+@*\.ru$")
   password: str = Field('ADMIN')



