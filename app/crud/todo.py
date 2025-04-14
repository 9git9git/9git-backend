from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.models.category import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse


# 할 일 생성
async def create_todo(
    db: AsyncSession, user_id: UUID, category_id: UUID, todo_data: TodoCreate
) -> TodoResponse:
    todo = Todo(
        user_id=user_id,
        category_id=category_id,
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
    return todo


# 특정 유저의 전체 할 일 목록 조회
async def read_all_todos(db: AsyncSession, user_id: UUID) -> List[TodoResponse]:
    result = await db.execute(select(Todo).where(Todo.user_id == user_id))
    return result.scalars().all()


# 특정 유저의 특정 할 일 조회 (응답용)
async def read_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> Optional[TodoResponse]:
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    return result.scalars().first()


# 특정 유저의 특정 할 일 조회 (내부 처리용)
async def read_raw_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> Optional[Todo]:
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    return result.scalars().first()


# 특정 유저의 특정 카테고리에 속한 할 일 목록 조회
async def read_todos_by_user_and_category(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[TodoResponse]:
    result = await db.execute(
        select(Todo).where(Todo.user_id == user_id, Todo.category_id == category_id)
    )
    return result.scalars().all()


# 수정
async def update_todo(
    db: AsyncSession, todo: Todo, todo_data: TodoUpdate
) -> TodoResponse:
    update_data = todo_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(todo, key, value)
    await db.commit()
    await db.refresh(todo)
    return todo


# 삭제
async def delete_todo(db: AsyncSession, todo: Todo) -> bool:
    delete_stmt = delete(Todo).where(Todo.id == todo.id)
    try:
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
