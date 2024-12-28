from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import async_session_maker
from app.db.models import Todo
from app.api.schemas.todo import Todolist


todo_router = APIRouter(
    prefix="/todo",
    tags=["ToDo"]
)


async def get_gb() -> AsyncSession:
    async with async_session_maker() as session:
        yield session


@todo_router.get("/{id}")
async def get_todos(id: int, db: AsyncSession = Depends(get_gb)):
    result = await db.get(Todo, id)
    if result:
        return result
    raise HTTPException(status_code=404, detail="Todo not found")


@todo_router.post("/")
async def create_todo(data: Todolist, db: AsyncSession = Depends(get_gb)):
    todo = Todo(
        title=data.title,
        description=data.description,
        completed=data.completed,
        important=data.important
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return todo


@todo_router.put("/{id}")
async def update_todo(id: int, data: Todolist, db: AsyncSession = Depends(get_gb)):
    result = await db.get(Todo, id)
    if result:
        result.title = data.title
        result.description = data.description
        result.completed = data.completed
        result.important = data.important
        await db.commit()
        await db.refresh(result)
        return result
    raise HTTPException(status_code=404, detail="Todo not found")


@todo_router.delete("/{id}")
async def delete_todo(id: int, db: AsyncSession = Depends(get_gb)):
    result = await db.get(Todo, id)
    if result:
        await db.delete(result)
        await db.commit()
        return {"message": "Todo deleted successfully"}
    raise HTTPException(status_code=404, detail="Todo not found")

