from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import HTTPException
from uuid import UUID
from typing import Optional, List

from app.models.category import CategoryProgress
from app.schemas.category_progress import CategoryProgressCreate, CategoryProgressUpdate
from app.utils.category_progress import calculate_progress_rate


# 카테고리 진행률 생성
async def create_category_progress(
    db: AsyncSession, progress_data: CategoryProgressCreate
) -> CategoryProgress:
    # 진행률 자동 계산
    progress_rate = calculate_progress_rate(
        progress_data.completed_goal, progress_data.total_goal
    )

    # 모델 인스턴스 생성 (Pydantic → SQLAlchemy)
    new_progress = CategoryProgress(
        **progress_data.model_dump(),  # user_id, category_name, total_goal, completed_goal
        progress_rate=progress_rate,
    )

    # DB에 추가 및 커밋
    db.add(new_progress)
    await db.commit()
    await db.refresh(new_progress)

    return new_progress


# ID 기준 단일 조회/ 특정 진행률 하나를 식별하기 위함
async def read_category_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> Optional[CategoryProgress]:
    result = await db.execute(
        select(CategoryProgress).where(CategoryProgress.id == progress_id)
    )
    return result.scalars().first()


# 특정 사용자(user_id)의 전체 진행률 목록 조회
async def read_category_progresses_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[CategoryProgress]:
    result = await db.execute(
        select(CategoryProgress).where(CategoryProgress.user_id == user_id)
    )
    return result.scalars().all()


# 진행률 정보 업데이트 (총 목표 / 완료 수 변경 시 진행률도 재계산)
async def update_category_progress(
    db: AsyncSession, progress_id: UUID, progress_data: CategoryProgressUpdate
) -> CategoryProgress:
    db_progress = await read_category_progress_by_id(db, progress_id)
    if not db_progress:
        raise HTTPException(status_code=404, detail="진행 정보가 존재하지 않습니다.")

    # 변경된 데이터만 추출해서 모델에 반영
    update_data = progress_data.model_dump(
        exclude_unset=True
    )  # 요청한 값만 변동되게 조건 걸어줌

    # 모델 소겅 업데이트
    for key, value in update_data.items():
        setattr(db_progress, key, value)

    # 진행률 자동 재계산
    db_progress.progress_rate = calculate_progress_rate(
        db_progress.completed_goal, db_progress.total_goal
    )

    await db.commit()
    await db.refresh(db_progress)

    return db_progress


# 진행률 정보 삭제
async def delete_category_progress(db: AsyncSession, progress_id: UUID) -> bool:
    progress = await read_category_progress_by_id(db, progress_id)
    if not progress:
        raise HTTPException(status_code=404, detail="진행 정보를 찾을 수 없습니다.")

    await db.delete(progress)
    await db.commit()

    return True
