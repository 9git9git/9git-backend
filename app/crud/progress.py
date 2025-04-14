from typing import List, Optional
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.category import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse


async def create_progress(
    db: AsyncSession, progress_data: ProgressCreate
) -> ProgressResponse:
    progress = Progress(
        user_id=progress_data.user_id,
        category_id=progress_data.category_id,
        start_date=progress_data.start_date,
        end_date=progress_data.end_date,
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return ProgressResponse.model_validate(progress)


async def read_all_progresses(db: AsyncSession) -> List[ProgressResponse]:
    result = await db.execute(select(Progress))
    progresses = result.scalars().all()
    return [ProgressResponse.model_validate(p) for p in progresses]


async def read_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[ProgressResponse]:
    result = await db.execute(select(Progress).where(Progress.id == progress_id))
    progress = result.scalars().first()
    return ProgressResponse.model_validate(progress) if progress else None


async def update_progress(
    db: AsyncSession, progress: Progress, progress_data: ProgressUpdate
) -> ProgressResponse:
    update_data = progress_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(progress, key, value)
    await db.commit()
    await db.refresh(progress)
    return ProgressResponse.model_validate(progress)


async def delete_progress(db: AsyncSession, progress: Progress) -> bool:
    delete_statement = delete(Progress).where(Progress.id == progress.id)

    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e

    return True
