from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from uuid import UUID
from typing import List, Optional

from app.models.evaluation import MonthlyAchievement
from app.schemas.monthly_achievement import (
    MonthlyAchievementCreate,
    MonthlyAchievementUpdate,
    MonthlyAchievementChart,
    MonthlyAchievementChartItem,
)
from app.utils.category_progress import calculate_progress_rate

# 비즈니스 로직에 필요한 임포트문
from fastapi import HTTPException
from sqlalchemy import select
from app.schemas.monthly_achievement import ComprehensiveEvaluationResult
from app.enum.category import CategoryNameEnum


# 월간 성취 정보 생성
async def register_monthly_achievement(
    db: AsyncSession, data: MonthlyAchievementCreate
) -> MonthlyAchievement:
    progress_rate = calculate_progress_rate(data.completed_goal, data.total_goal)

    new_record = MonthlyAchievement(
        **data.model_dump(),
        progress_rate=progress_rate,
    )
    db.add(new_record)
    await db.commit()
    await db.refresh(new_record)
    return new_record


# ID 기준 단일 조회
async def select_monthly_achievement_by_id(
    db: AsyncSession, achievement_id: UUID
) -> Optional[MonthlyAchievement]:
    result = await db.execute(
        select(MonthlyAchievement).where(MonthlyAchievement.id == achievement_id)
    )
    return result.scalars().first()


# 유저 기준 전체 조회
async def select_monthly_achievements_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[MonthlyAchievement]:
    result = await db.execute(
        select(MonthlyAchievement).where(MonthlyAchievement.user_id == user_id)
    )
    return result.scalars().all()


# 월간 성취 수정
async def update_monthly_achievement_by_id(
    db: AsyncSession,
    achievement_id: UUID,
    data: MonthlyAchievementUpdate,
) -> Optional[MonthlyAchievement]:
    record = await select_monthly_achievement_by_id(db, achievement_id)
    if not record:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(record, key, value)

    record.progress_rate = calculate_progress_rate(
        record.completed_goal, record.total_goal
    )

    await db.commit()
    await db.refresh(record)
    return record


# 월간 성취 삭제
async def delete_monthly_achievement_by_id(
    db: AsyncSession, achievement_id: UUID
) -> bool:
    record = await select_monthly_achievement_by_id(db, achievement_id)
    if not record:
        return False
    await db.delete(record)
    await db.commit()
    return True


# 비즈니스 로직: 월별 목표별 달성 현황 그래프용 데이터 반환
async def summarize_monthly_achievements_by_category(
    db: AsyncSession, user_id: UUID, category_name: str
) -> MonthlyAchievementChart:
    result = await db.execute(
        select(MonthlyAchievement).where(
            MonthlyAchievement.user_id == user_id,
            MonthlyAchievement.category_name == category_name,
        )
    )
    records = result.scalars().all()

    chart_items = [
        MonthlyAchievementChartItem(
            month=record.month_year.month,
            achievement_rate=float(record.progress_rate),
        )
        for record in records
    ]

    return MonthlyAchievementChart(
        category_name=category_name,
        monthly_progress=sorted(chart_items, key=lambda x: x.month),
    )


# 유저의 월별 성과 평가를 요약하는 비즈니스 로직
async def summarize_monthly_evaluation_by_user(
    db: AsyncSession, user_id: UUID
) -> ComprehensiveEvaluationResult:
    # 1. 해당 유저의 모든 월간 성취 데이터 조회
    result = await db.execute(
        select(MonthlyAchievement).where(MonthlyAchievement.user_id == user_id)
    )
    achievements: list[MonthlyAchievement] = result.scalars().all()

    if not achievements:
        raise HTTPException(status_code=404, detail="기록된 월간 성취가 없습니다.")

    # 2. 전체 평균 진행률 계산
    total_rate = sum([float(a.progress_rate) for a in achievements])
    overall = total_rate / len(achievements)

    # 3. 가장 성취율 높은 / 낮은 카테고리 찾기
    best = max(achievements, key=lambda x: x.progress_rate)
    worst = min(achievements, key=lambda x: x.progress_rate)

    # 4. 응답 데이터 구성
    return ComprehensiveEvaluationResult(
        overall_achievement_rate=round(overall, 2),
        evaluation_text="전체적으로 목표를 잘 달성하고 있어요!",
        strength_category=best.category_name,
        strength_achievement_rate=float(best.progress_rate),
        strength_text="이 카테고리에서는 아주 잘하고 있어요!",
        improvement_category=worst.category_name,
        improvement_achievement_rate=float(worst.progress_rate),
        improvement_text="이 카테고리는 조금 더 노력해볼까요?",
    )


# 비즈니스 로직 - 사용자별 카테고리 월별 목표 달성률 요약 (그래프용)
async def summarize_monthly_progress_chart_by_user(
    db: AsyncSession, user_id: UUID, category_name: CategoryNameEnum
) -> MonthlyAchievementChart:
    result = await db.execute(
        select(MonthlyAchievement).where(
            MonthlyAchievement.user_id == user_id,
            MonthlyAchievement.category_name == category_name,
        )
    )
    records: List[MonthlyAchievement] = result.scalars().all()

    # 정렬 후 달성률 데이터 생성
    progress_items = [
        MonthlyAchievementChartItem(
            month=record.month_year.month,
            achievement_rate=float(record.progress_rate),
        )
        for record in sorted(records, key=lambda r: r.month_year)
    ]

    return MonthlyAchievementChart(
        category_name=category_name, monthly_progress=progress_items
    )
