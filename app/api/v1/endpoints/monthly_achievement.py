from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.base import ResponseBase
from app.schemas.monthly_achievement import (
    MonthlyAchievementCreate,
    MonthlyAchievementUpdate,
    MonthlyAchievementResponse,
    MonthlyAchievementChart,
    ComprehensiveEvaluationResult,
)
from app.services.monthly_achievement import (
    select_monthly_achievement_by_id,
    select_monthly_achievements_by_user_id,
    register_monthly_achievement,
    update_monthly_achievement_by_id,
    delete_monthly_achievement_by_id,
    summarize_monthly_evaluation_by_user,
    summarize_monthly_progress_chart_by_user,
)
from app.enum.category import CategoryNameEnum

router = APIRouter()


# 단일 조회
@router.get(
    "/{achievement_id}", response_model=ResponseBase[MonthlyAchievementResponse]
)
async def get_monthly_achievement_by_id(
    achievement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MonthlyAchievementResponse]:
    try:
        result = await select_monthly_achievement_by_id(db, achievement_id)
        if not result:
            return ResponseBase(
                status_code=404, error="해당 데이터를 찾을 수 없습니다."
            )
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 전체 조회 (특정 유저 기준)
@router.get(
    "/user/{user_id}", response_model=ResponseBase[List[MonthlyAchievementResponse]]
)
async def get_monthly_achievements_by_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[MonthlyAchievementResponse]]:
    try:
        result = await select_monthly_achievements_by_user_id(db, user_id)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 생성
@router.post("/", response_model=ResponseBase[MonthlyAchievementResponse])
async def post_monthly_achievement(
    request_data: MonthlyAchievementCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MonthlyAchievementResponse]:
    try:
        result = await register_monthly_achievement(db, request_data)
        return ResponseBase(status_code=201, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 수정
@router.put(
    "/{achievement_id}", response_model=ResponseBase[MonthlyAchievementResponse]
)
async def put_monthly_achievement(
    achievement_id: UUID,
    update_data: MonthlyAchievementUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MonthlyAchievementResponse]:
    try:
        result = await update_monthly_achievement_by_id(db, achievement_id, update_data)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 삭제
@router.delete("/{achievement_id}", response_model=ResponseBase[bool])
async def delete_monthly_achievement(
    achievement_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_monthly_achievement_by_id(db, achievement_id)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 비즈니스 로직 - 월별 종합 평가 조회
@router.get(
    "/user/{user_id}/evaluation",
    response_model=ResponseBase[ComprehensiveEvaluationResult],
)
async def get_monthly_evaluation_summary(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResult]:
    try:
        result = await summarize_monthly_evaluation_by_user(db, user_id)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 비즈니스 로직 - 카테고리별 월간 달성률 그래프
@router.get(
    "/user/{user_id}/chart", response_model=ResponseBase[List[MonthlyAchievementChart]]
)
async def get_monthly_achievement_chart(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[MonthlyAchievementChart]]:
    try:
        result = await summarize_monthly_progress_chart_by_user(db, user_id)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 비즈니스 로직 - 종합 평가 요약 조회
@router.get(
    "/summary/evaluation/{user_id}",
    response_model=ResponseBase[ComprehensiveEvaluationResult],
    summary="월별 종합 평가 요약 조회",
)
async def get_monthly_evaluation_summary(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResult]:
    try:
        evaluation = await summarize_monthly_evaluation_by_user(db, user_id)
        return ResponseBase(status_code=200, data=evaluation)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 비즈니스 로직 = 월별 달성률 그래프 / 특정 유저의 카테고리별 월간 달성률 데이터 조회
@router.get(
    "/chart/{user_id}/{category_name}",
    response_model=ResponseBase[MonthlyAchievementChart],
)
async def get_monthly_achievement_chart_by_user(
    user_id: UUID,
    category_name: CategoryNameEnum,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MonthlyAchievementChart]:
    try:
        chart = await summarize_monthly_progress_chart_by_user(
            db, user_id, category_name
        )
        return ResponseBase(status_code=200, data=chart)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))
