from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from sqlalchemy.orm import selectinload
from app.models.category import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse


# 진행 생성
async def create_progress(
    db: AsyncSession, user_id: UUID, progress_data: ProgressCreate
) -> ProgressResponse:
    progress = Progress(
        user_id=user_id,
        category_id=progress_data.categoryId,
        start_date=progress_data.startDate,
        end_date=progress_data.endDate,
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return progress


# 전체 진행 조회
async def read_all_progresses(
    db: AsyncSession, user_id: UUID
) -> List[ProgressResponse]:
    result = await db.execute(
        select(Progress)
        .options(selectinload(Progress.category))
        .where(Progress.user_id == user_id)
    )
    return result.scalars().all()


# ID로 진행 조회
async def read_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[ProgressResponse]:
    result = await db.execute(
        select(Progress)
        .options(selectinload(Progress.category))
        .where(Progress.id == progress_id)
    )
    return result.scalars().first()


# 진행 수정
async def update_progress(
    db: AsyncSession, progress: Progress, progress_data: ProgressUpdate
) -> ProgressResponse:
    update_data = progress_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(progress, key, value)

    await db.commit()
    await db.refresh(progress)
    return progress


# 진행 삭제
async def delete_progress(db: AsyncSession, progress: Progress) -> bool:
    delete_statement = delete(Progress).where(Progress.id == progress.id)

    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

    return True
