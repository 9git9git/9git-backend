from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.crud.category_progress import (
    read_category_progress_by_id,
    read_category_progresses_by_user_id,
    create_category_progress,
    update_category_progress,
    delete_category_progress,
)
from app.schemas.category_progress import (
    CategoryProgressCreate,
    CategoryProgressUpdate,
)
from app.models.category import CategoryProgress


# ID 기준 단일 조회
async def select_category_progress_by_id(
    db: AsyncSession, progress_id: UUID
) -> CategoryProgress:
    return await read_category_progress_by_id(db, progress_id)


# 특정 유저의 전체 카테고리 진행률 조회
async def select_category_progresses_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[CategoryProgress]:
    return await read_category_progresses_by_user_id(db, user_id)


# 카테고리 진행률 생성
async def register_category_progress(
    db: AsyncSession, progress_data: CategoryProgressCreate
) -> CategoryProgress:
    return await create_category_progress(db, progress_data)


# 카테고리 진행률 수정
async def update_category_progress_by_id(
    db: AsyncSession, progress_id: UUID, progress_data: CategoryProgressUpdate
) -> CategoryProgress:
    return await update_category_progress(db, progress_id, progress_data)


# 카테고리 진행률 삭제
async def delete_category_progress_by_id(db: AsyncSession, progress_id: UUID) -> bool:
    return await delete_category_progress(db, progress_id)


# 비즈니스 로직 : 카테고리 진행률 조회

from sqlalchemy import select
from app.schemas.category_progress import GoalProgressItem, GoalProgressSummary
from app.utils.messages import get_random_encouragement_message


# 유저의 전체 카테고리 진행률 요약 조회
async def summarize_category_progresses_by_user_id(
    db: AsyncSession, user_id: UUID
) -> GoalProgressSummary:
    # 1. 해당 유저의 모든 카테고리 진행 정보 조회
    result = await db.execute(
        select(CategoryProgress).where(CategoryProgress.user_id == user_id)
    )
    progresses: list[CategoryProgress] = result.scalars().all()

    if not progresses:
        return GoalProgressSummary(
            main_message="아직 설정한 목표가 없어요!",
            main_progress_rate=0.0,
            details=[],
        )

    # 2. 카테고리별 진행률 아이템 생성
    detail_items = [
        GoalProgressItem(
            category_name=progress.category_name,
            progress_rate=float(progress.progress_rate),
        )
        for progress in progresses
    ]

    # 3. 전체 평균 진행률 계산
    total_rate = sum([float(p.progress_rate) for p in progresses])
    main_rate = total_rate / len(progresses)

    # 4. 랜덤 메시지 선택
    message = get_random_encouragement_message()

    # 5. 최종 응답 스키마 구성
    return GoalProgressSummary(
        main_message=message,
        main_progress_rate=round(main_rate, 2),
        details=detail_items,
    )
