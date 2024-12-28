from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str


class Todolist(BaseModel):
    title: str
    description: str
    completed: bool = False
    important: bool = False
