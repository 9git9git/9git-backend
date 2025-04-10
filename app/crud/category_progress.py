from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from uuid import UUID
from typing import Optional, List

from app.models.category import CategoryProgress
from app.schemas.category_progress import CategoryProgressCreate, CategoryProgressUpdate
from app.utils.category_progress import calculate_progress_rate


# 진행정보 생성 (진행률 자동 계산)
async def create_category_progress(
    db: AsyncSession, progress_data: CategoryProgressCreate
) -> CategoryProgress:
    progress_rate = calculate_progress_rate(
        progress_data.completed_goal,
        progress_data.total_goal,
    )

    new_progress = CategoryProgress(
        **progress_data.model_dump(),
        progress_rate=progress_rate,
    )

    db.add(new_progress)
    await db.commit()
    await db.refresh(new_progress)

    return new_progress


# ID로 단일 조회
async def read_category_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[CategoryProgress]:
    result = await db.execute(
        select(CategoryProgress).where(CategoryProgress.id == progress_id)
    )
    return result.scalars().first()


# 특정 사용자(user_id)의 진행정보 전체 조회
async def read_category_progresses_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[CategoryProgress]:
    result = await db.execute(
        select(CategoryProgress).where(CategoryProgress.user_id == user_id)
    )
    return result.scalars().all()


# 진행정보 수정 (변경된 값 기준으로 자동 재계산)
async def update_category_progress(
    db: AsyncSession, progress_id: UUID, progress_data: CategoryProgressUpdate
) -> CategoryProgress:
    db_progress = await read_category_progress_by_id(db, progress_id)
    if not db_progress:
        raise HTTPException(
            status_code=404, detail="카테고리 진행 정보를 찾을 수 없습니다."
        )

    # 수정 요청된 필드만 반영
    update_data = progress_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_progress, key, value)

    # 유틸 함수로 자동 재계산
    db_progress.progress_rate = calculate_progress_rate(
        db_progress.completed_goal,
        db_progress.total_goal,
    )

    await db.commit()
    await db.refresh(db_progress)

    return db_progress


# 삭제
async def delete_category_progress(db: AsyncSession, progress_id: UUID) -> bool:
    db_progress = await read_category_progress_by_id(db, progress_id)
    if not db_progress:
        raise HTTPException(
            status_code=404, detail="카테고리 진행 정보를 찾을 수 없습니다."
        )

    await db.delete(db_progress)
    await db.commit()

    return True
