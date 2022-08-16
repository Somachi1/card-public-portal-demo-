from pydantic import BaseModel
from typing import Optional



class User(BaseModel):
    email: str

class UserCreate(User):
    password: str
    

class UserResponse(User):
    password: str
    pass

    class Config:
        orm_mode = True

