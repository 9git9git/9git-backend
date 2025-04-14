from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.week import WeekCreate, WeekResponse, WeekUpdate
from app.services.week import (
    add_week_service,
    delete_week_service,
    edit_week_service,
    select_week_by_id_service,
    select_weeks_service,
)
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from app.schemas.base import ResponseBase
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=ResponseBase[List[WeekResponse]])
async def get_weeks(
    todo_id: UUID, db: AsyncSession = Depends(get_db)
) -> ResponseBase[List[WeekResponse]]:
    try:
        weeks = await select_weeks_service(db, todo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=weeks)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)

    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{week_id}", response_model=ResponseBase[WeekResponse])
async def get_week_by_id(
    todo_id: UUID,
    week_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[WeekResponse]:
    try:
        week = await select_week_by_id_service(db, todo_id, week_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=week)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/", response_model=ResponseBase[WeekResponse])
async def post_week(
    week: WeekCreate,
    todo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[WeekResponse]:
    try:
        week = await add_week_service(db, todo_id, week)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=week)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{week_id}", response_model=ResponseBase[WeekResponse])
async def put_week(
    todo_id: UUID,
    week_id: UUID,
    week: WeekUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[WeekResponse]:
    try:
        week = await edit_week_service(db, todo_id, week_id, week)
        return ResponseBase(status_code=status.HTTP_200_OK, data=week)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{week_id}", response_model=ResponseBase[bool])
async def delete_week(
    todo_id: UUID,
    week_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_week_service(db, todo_id, week_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
