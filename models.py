from pydantic import BaseModel, EmailStr
from typing import Optional

class User(BaseModel):
    email: EmailStr
    password: str

class UserInDB(User):
    _id: Optional[str]

class Todo(BaseModel):
    title: str
    completed: bool = False
    user_email: str
