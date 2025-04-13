from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse
from app.crud.progress import (
    create_progress,
    read_all_progresses,
    read_progress_by_id,
    update_progress,
    delete_progress,
)


async def add_progress(
    db: AsyncSession, progress_data: ProgressCreate
) -> ProgressResponse:
    progress = await create_progress(db, progress_data)
    return progress


async def select_all_progresses(db: AsyncSession) -> List[ProgressResponse]:
    return await read_all_progresses(db)


async def select_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> ProgressResponse:
    progress = await read_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="진행률을 찾을 수 없습니다.",
        )
    return progress


async def update_progress_by_id(
    db: AsyncSession, progress_id: UUID, progress_data: ProgressUpdate
) -> ProgressResponse:
    progress = await read_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="진행률을 찾을 수 없습니다.",
        )
    updated = await update_progress(db, progress, progress_data)
    return updated


async def delete_progress_by_id(db: AsyncSession, progress_id: UUID) -> bool:
    progress = await read_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="진행률을 찾을 수 없습니다.",
        )
    return await delete_progress(db, progress)
