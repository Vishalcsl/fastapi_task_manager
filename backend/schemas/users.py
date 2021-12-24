from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    firstname: str
    lastname: str = None
    email: EmailStr
    password: str

class ShowUser(BaseModel):
    username: str
    email: EmailStr
    is_active: bool

    #tells pydantic to convert even non dict obj to json 
    class Config():
        orm_mode = True