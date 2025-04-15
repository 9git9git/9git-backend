from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.schemas.base import ResponseBase
from app.services.todo import (
    add_todo,
    select_all_todos,
    select_todo_by_id,
    select_todos_by_date_range,
    update_todo_by_id,
    delete_todo_service,
)
from app.db.session import get_db

router = APIRouter()


# 할 일 생성
@router.post("/", response_model=ResponseBase[TodoResponse])
async def create_todo(
    user_id: UUID,
    category_id: UUID,
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await add_todo(db, user_id, category_id, todo_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


# 전체 할 일 조회 (유저 기준)
@router.get("/", response_model=ResponseBase[List[TodoResponse]])
async def get_all_todos(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[TodoResponse]]:
    try:
        todos = await select_all_todos(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todos)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


# 날짜 범위로 할 일 조회
@router.get("/date-range", response_model=ResponseBase[List[TodoResponse]])
async def get_todos_by_date_range(
    user_id: UUID,
    startDate: date = Query(..., description="시작 날짜 (YYYY-MM-DD)"),
    endDate: date = Query(..., description="종료 날짜 (YYYY-MM-DD)"),
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[TodoResponse]]:
    try:
        todos = await select_todos_by_date_range(db, user_id, startDate, endDate)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todos)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


# 특정 할 일 조회
@router.get("/{todo_id}", response_model=ResponseBase[TodoResponse])
async def get_todo_by_id(
    user_id: UUID,
    todo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await select_todo_by_id(db, user_id, todo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


# 할 일 수정
@router.put("/{todo_id}", response_model=ResponseBase[TodoResponse])
async def update_todo(
    user_id: UUID,
    todo_id: UUID,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await update_todo_by_id(db, user_id, todo_id, todo_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


# 할 일 삭제
@router.delete("/{todo_id}", response_model=ResponseBase[bool])
async def delete_todo(
    user_id: UUID,
    todo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_todo_service(db, user_id, todo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )
