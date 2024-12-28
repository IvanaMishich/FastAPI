from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from fastapi.exception_handlers import (
    http_exception_handler,
    request_validation_exception_handler,
)
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional


app = FastAPI()

userlist = [{"username": "user1", "password": "pass1"},
            {"username": "user2", "password": "pass2"}]

class User(BaseModel):
    username: str
    password: constr(min_length=8, max_length=16)

class ErrorResponseModel(BaseModel):
    status_code: int
    message: str
    error_code: str


@app.exception_handler(RequestValidationError)
async def validation(request, exc):
    print("Некорректное значение")
    return await request_validation_exception_handler(request, exc)


@app.post("/registration/")
async def registration(user: User):
    for c in userlist:
        if c.get("username") == user.username and c.get("password") == user.password:
            return c
    return raise


@app.get("/user/")
async def users(user: User)

