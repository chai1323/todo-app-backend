# schemas.py
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TodoCreate(BaseModel):
    title: str

class TodoResponse(BaseModel):
    id: str
    title: str
    completed: bool
    user_email: Optional[EmailStr] = None
    timestamp: Optional[datetime] = None
