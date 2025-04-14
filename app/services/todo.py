from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.crud.todo import (
    create_todo,
    read_all_todos,
    read_todo_by_id,
    read_raw_todo_by_id,
    update_todo,
    delete_todo,
)


async def add_todo(db: AsyncSession, todo_data: TodoCreate) -> TodoResponse:
    try:
        return await create_todo(db, todo_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="할 일 생성 중 오류가 발생했습니다.",
        ) from e


async def select_all_todos(db: AsyncSession) -> List[TodoResponse]:
    return await read_all_todos(db)


async def select_todo_by_id(db: AsyncSession, todo_id: UUID) -> TodoResponse:
    todo = await read_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다.",
        )
    return todo


async def update_todo_by_id(
    db: AsyncSession, todo_id: UUID, todo_data: TodoUpdate
) -> TodoResponse:
    todo = await read_raw_todo_by_id(db, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="할 일을 찾을 수 없습니다.",
        )

    try:
        return await update_todo(db, todo, todo_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="할 일 수정 중 오류가 발생했습니다.",
        ) from e


async def delete_todo_service(db: AsyncSession, todo_id: UUID) -> bool:
    try:
        todo = await read_raw_todo_by_id(db, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="할 일을 찾을 수 없습니다.",
            )
        return await delete_todo(db, todo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="할 일 삭제 중 오류가 발생했습니다.",
        ) from e
