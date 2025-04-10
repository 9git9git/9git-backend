from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional

from app.crud.category_progress import (
    read_category_progress_by_id,
    read_category_progresses_by_user_id,
    create_category_progress,
    update_category_progress,
    delete_category_progress,
)
from app.schemas.category_progress import CategoryProgressCreate, CategoryProgressUpdate
from app.models.category import CategoryProgress


# ✅ ID로 단일 조회
async def select_category_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[CategoryProgress]:
    return await read_category_progress_by_id(db, progress_id)


# ✅ user_id 기준으로 전체 조회
async def select_category_progresses_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[CategoryProgress]:
    return await read_category_progresses_by_user_id(db, user_id)


# ✅ 생성
async def register_category_progress(
    db: AsyncSession, progress_data: CategoryProgressCreate
) -> CategoryProgress:
    return await create_category_progress(db, progress_data)


# ✅ 수정
async def update_category_progress_by_id(
    db: AsyncSession, progress_id: UUID, progress_data: CategoryProgressUpdate
) -> CategoryProgress:
    return await update_category_progress(db, progress_id, progress_data)


# ✅ 삭제
async def delete_category_progress_by_id(db: AsyncSession, progress_id: UUID) -> bool:
    return await delete_category_progress(db, progress_id)
