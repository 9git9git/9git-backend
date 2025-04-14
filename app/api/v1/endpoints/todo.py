from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.schemas.base import ResponseBase
from app.services.todo import (
    add_todo,
    select_all_todos,
    select_todo_by_id,
    update_todo_by_id,
    delete_todo_service,
)
from app.db.session import get_db

router = APIRouter(prefix="/todos", tags=["Todo"])


@router.post("/", response_model=ResponseBase[TodoResponse])
async def create_todo(
    todo_data: TodoCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await add_todo(db, todo_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


@router.get("/", response_model=ResponseBase[List[TodoResponse]])
async def get_all_todos(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[TodoResponse]]:
    try:
        todos = await select_all_todos(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todos)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


@router.get("/{todo_id}", response_model=ResponseBase[TodoResponse])
async def get_todo_by_id(
    todo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await select_todo_by_id(db, todo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


@router.patch("/{todo_id}", response_model=ResponseBase[TodoResponse])
async def update_todo(
    todo_id: UUID,
    todo_data: TodoUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodoResponse]:
    try:
        todo = await update_todo_by_id(db, todo_id, todo_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=todo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )


@router.delete("/{todo_id}", response_model=ResponseBase[bool])
async def delete_todo(
    todo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_todo_service(db, todo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error=str(e),
        )
