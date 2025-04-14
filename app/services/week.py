from app.crud.week import (
    delete_week,
    read_week_by_id,
    read_weeks,
    create_week,
    update_week,
)
from app.schemas.week import WeekCreate, WeekResponse, WeekUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from fastapi import HTTPException, status


async def select_weeks_service(db: AsyncSession, todo_id: UUID) -> List[WeekResponse]:
    return await read_weeks(db, todo_id)


async def select_week_by_id_service(
    db: AsyncSession, todo_id: UUID, week_id: UUID
) -> WeekResponse:
    return await read_week_by_id(db, todo_id, week_id)


async def add_week_service(
    db: AsyncSession, todo_id: UUID, week_data: WeekCreate
) -> WeekResponse:
    return await create_week(db, todo_id, week_data)


async def edit_week_service(
    db: AsyncSession, todo_id: UUID, week_id: UUID, week_data: WeekUpdate
) -> WeekResponse:
    try:
        db_week = await read_week_by_id(db, todo_id, week_id)
        if not db_week:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 요일을 찾을 수 없습니다.",
            )
        return await update_week(db, todo_id, week_id, week_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 오류가 발생했습니다.",
        ) from e


async def delete_week_service(db: AsyncSession, todo_id: UUID, week_id: UUID) -> bool:
    try:
        db_week = await read_week_by_id(db, todo_id, week_id)
        if not db_week:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="해당 요일을 찾을 수 없습니다.",
            )
        return await delete_week(db, todo_id, week_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 오류가 발생했습니다.",
        ) from e
