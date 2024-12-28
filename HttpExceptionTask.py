from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional


app = FastAPI()


class React(BaseModel):
    error_code: int
    error_message: str
    error_details: Optional[str] = None


class CustomExceptionA(HTTPException):
    def __init__(self, detail: str, status_code: int = 404):
        super().__init__(status_code=status_code, detail=detail)


class CustomExceptionB(HTTPException):
    def __init__(self, detail: str, status_code: int = 400):
        super().__init__(status_code=status_code, detail=detail)


# Обработчики ошибок
@app.exception_handler(CustomExceptionA)
async def custom_exception_handler_a(request: Request, exc: React):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error A": exc.detail}
    )


@app.exception_handler(CustomExceptionB)
async def custom_exception_handler_b(request: Request, exc: React):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error B": exc.detail}
    )


# Обработчик глобальных исключений, который "ловит" все необработанные исключения
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )


@app.get("/items/{item_id}/", response_model=React)
async def read_item_a(item_id: int):
    if item_id == 42:
        raise CustomExceptionA(detail="Item not found", status_code=404)
    return {"item_id": item_id}


@app.get("/root/", response_model=React)
async def read_item_b():
    raise CustomExceptionB(detail="Bad request", status_code=400)
