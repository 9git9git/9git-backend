from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, extract
from uuid import UUID
from typing import Optional, List
from app.models.evaluation import MonthlyAchievement
from app.schemas.monthly_achievement import (
    MonthlyAchievementCreate,
    MonthlyAchievementUpdate,
    MonthlyAchievementChartItem,
    MonthlyAchievementChart,
)
from app.utils.category_progress import calculate_progress_rate


# 생성
async def create_monthly_achievement(
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


# 단일 조회
async def read_monthly_achievement_by_id(
    db: AsyncSession, achievement_id: UUID
) -> Optional[MonthlyAchievement]:
    result = await db.execute(
        select(MonthlyAchievement).where(MonthlyAchievement.id == achievement_id)
    )
    return result.scalars().first()


# 유저 기준 전체 조회
async def read_monthly_achievements_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[MonthlyAchievement]:
    result = await db.execute(
        select(MonthlyAchievement).where(MonthlyAchievement.user_id == user_id)
    )
    return result.scalars().all()


# 업데이트
async def update_monthly_achievement(
    db: AsyncSession, achievement_id: UUID, data: MonthlyAchievementUpdate
) -> MonthlyAchievement:
    achievement = await read_monthly_achievement_by_id(db, achievement_id)
    if not achievement:
        return None

    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(achievement, key, value)

    # 진행률 재계산
    achievement.progress_rate = calculate_progress_rate(
        achievement.completed_goal, achievement.total_goal
    )

    await db.commit()
    await db.refresh(achievement)
    return achievement


# 삭제
async def delete_monthly_achievement(db: AsyncSession, achievement_id: UUID) -> bool:
    achievement = await read_monthly_achievement_by_id(db, achievement_id)
    if not achievement:
        return False

    await db.delete(achievement)
    await db.commit()
    return True


# 월별 목표별 달성 현황 (그래프)
async def get_monthly_chart_data(
    db: AsyncSession, user_id: UUID, category_name: str
) -> MonthlyAchievementChart:
    result = await db.execute(
        select(MonthlyAchievement).where(
            MonthlyAchievement.user_id == user_id,
            MonthlyAchievement.category_name == category_name,
        )
    )
    items = result.scalars().all()

    chart_items = [
        MonthlyAchievementChartItem(
            month=record.month_year.month,
            achievement_rate=float(record.progress_rate),
        )
        for record in items
    ]

    return MonthlyAchievementChart(
        category_name=category_name,
        monthly_progress=sorted(chart_items, key=lambda x: x.month),
    )
