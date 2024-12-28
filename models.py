from pydantic import BaseModel, PositiveInt, EmailStr
from typing import Literal


class User(BaseModel):
    name: str
    email: EmailStr
    age: PositiveInt | None = None
    is_subscribed: bool = False


class User2(BaseModel):
    username: str
    password: str


class User3(BaseModel):
    username: str
    password: str
    role: Literal["admin", "user", "guest"] | None
    permission: str | None = None


class Feedback(BaseModel):
    name: str
    message: str


class Todo(BaseModel):
    title: str
    description: str
    completed: bool = False
