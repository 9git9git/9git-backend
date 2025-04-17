from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.services.chart import get_daily_achievement, get_monthly_achievement
from app.schemas.chart import DailyAchievementResponse, MonthlyAchievementResponse
from app.schemas.base import ResponseBase

router = APIRouter()


@router.get("/chart/daily", response_model=ResponseBase[List[DailyAchievementResponse]])
async def get_daily_chart_data(
    user_id: UUID,
    year: int = Query(..., description="연도 기준 필터 (예: 2025)"),
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[DailyAchievementResponse]]:
    try:
        data = await get_daily_achievement(db, user_id=user_id, year=year)
        return ResponseBase(status_code=status.HTTP_200_OK, data=data)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="일별 차트 데이터를 가져오는 중 오류가 발생했습니다.",
        )


@router.get(
    "/chart/monthly", response_model=ResponseBase[List[MonthlyAchievementResponse]]
)
async def get_monthly_chart_data(
    user_id: UUID,
    year: int = Query(..., description="연도 기준 필터 (예: 2025)"),
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[MonthlyAchievementResponse]]:
    try:
        data = await get_monthly_achievement(db, user_id=user_id, year=year)
        return ResponseBase(status_code=status.HTTP_200_OK, data=data)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="월별 차트 데이터를 가져오는 중 오류가 발생했습니다.",
        )
