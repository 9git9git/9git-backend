from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional

from app.models.category import Progress
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse


async def create_progress(db: AsyncSession, progress_data: ProgressCreate) -> Progress:
    progress = Progress(
        user_id=progress_data.user_id,
        category_id=progress_data.category_id,
        start_date=progress_data.start_date,
        end_date=progress_data.end_date,
    )
    db.add(progress)
    await db.commit()
    await db.refresh(progress)
    return progress


async def read_all_progresses(db: AsyncSession) -> List[Progress]:
    result = await db.execute(select(Progress))
    return result.scalars().all()


async def read_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[Progress]:
    result = await db.execute(select(Progress).where(Progress.id == progress_id))
    return result.scalars().first()


async def update_progress(
    db: AsyncSession, progress: Progress, progress_data: ProgressUpdate
) -> Progress:
    update_data = progress_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(progress, key, value)
    await db.commit()
    await db.refresh(progress)
    return progress


async def delete_progress(db: AsyncSession, progress: Progress) -> bool:
    await db.execute(delete(Progress).where(Progress.id == progress.id))
    await db.commit()
    return True
