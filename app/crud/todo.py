from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.models.category import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


async def create_todo(db: AsyncSession, todo_data: TodoCreate) -> TodoResponse:
    todo = Todo(
        user_id=todo_data.userId,
        category_id=todo_data.categoryId,
        week_id=todo_data.weekId,
        content=todo_data.content,
        start_date=todo_data.startDate,
        end_date=todo_data.endDate,
        is_completed=todo_data.isCompleted,
        is_repeat=todo_data.isRepeat,
    )
    db.add(todo)
    await db.commit()
    await db.refresh(todo)
    return TodoResponse.model_validate(todo)


async def read_all_todos(db: AsyncSession) -> List[TodoResponse]:
    result = await db.execute(select(Todo))
    todos = result.scalars().all()
    return [TodoResponse.model_validate(todo) for todo in todos]


async def read_todo_by_id(db: AsyncSession, todo_id: UUID) -> Optional[TodoResponse]:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    todo = result.scalars().first()
    return TodoResponse.model_validate(todo) if todo else None


async def read_raw_todo_by_id(db: AsyncSession, todo_id: UUID) -> Optional[Todo]:
    result = await db.execute(select(Todo).where(Todo.id == todo_id))
    return result.scalars().first()


async def update_todo(
    db: AsyncSession, todo: Todo, todo_data: TodoUpdate
) -> TodoResponse:
    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return TodoResponse.model_validate(todo)


async def delete_todo(db: AsyncSession, todo: Todo) -> bool:
    delete_stmt = delete(Todo).where(Todo.id == todo.id)
    try:
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
