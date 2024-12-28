from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import BaseModel, EmailStr, conint, constr
from typing import Optional


app = FastAPI()


class User(BaseModel):
    username: str
    age: conint(gt=18)
    email: EmailStr
    password: constr(min_length=8, max_length=16)
    phone: Optional[str] = 'Unknown'


@app.exception_handler(RequestValidationError)
async def value(request, exc):
    return JSONResponse(status_code=422, content={"error": str(exc.errors())})


@app.post("/users/")
async def user(user: User):
    return user
