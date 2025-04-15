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
    read_todos_by_user_and_category,
)


# ✅ 할 일 생성
async def add_todo(
    db: AsyncSession, user_id: UUID, category_id: UUID, todo_data: TodoCreate
) -> TodoResponse:
    try:
        return await create_todo(db, user_id, category_id, todo_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


# ✅ 특정 유저의 전체 할 일 목록 조회
async def select_all_todos(db: AsyncSession, user_id: UUID) -> List[TodoResponse]:
    return await read_all_todos(db, user_id)


# ✅ 특정 유저의 특정 할 일 조회
async def select_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> TodoResponse:
    todo = await read_todo_by_id(db, user_id, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )
    return todo


# ✅ 유저 + 카테고리별 Todo 목록 조회
async def select_todos_by_user_and_category(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[TodoResponse]:
    return await read_todos_by_user_and_category(db, user_id, category_id)


# ✅ 할 일 수정
async def update_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID, todo_data: TodoUpdate
) -> TodoResponse:
    todo = await read_raw_todo_by_id(db, user_id, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )
    return await update_todo(db, todo, todo_data)


# ✅ 할 일 삭제
async def delete_todo_service(db: AsyncSession, user_id: UUID, todo_id: UUID) -> bool:
    try:
        todo = await read_raw_todo_by_id(db, user_id, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo를 찾을 수 없습니다.",
            )
        return await delete_todo(db, todo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
