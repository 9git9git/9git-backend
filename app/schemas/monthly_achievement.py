from uuid import UUID
from datetime import date
from decimal import Decimal
from typing import Optional
from app.schemas.base import BaseModel
from app.enum.category import CategoryNameEnum


# 생성 요청용
class MonthlyAchievementCreate(BaseModel):
    user_id: UUID
    progress_id: UUID
    category_name: CategoryNameEnum
    month_year: date
    total_goal: Optional[int] = 0
    completed_goal: Optional[int] = 0


# 수정 요청용
class MonthlyAchievementUpdate(BaseModel):
    total_goal: Optional[int] = None
    completed_goal: Optional[int] = None


# 조회 응답용
class MonthlyAchievementResponse(BaseModel):
    id: UUID
    user_id: UUID
    progress_id: UUID
    category_name: CategoryNameEnum
    month_year: date
    total_goal: int
    completed_goal: int
    progress_rate: Decimal


# 월별 종합평가
class ComprehensiveEvaluationResult(BaseModel):
    overall_achievement_rate: float  # 전체 달성률 (%)
    evaluation_text: str  # 예: "꾸준한 노력으로 목표를 잘 달성하고 있어요!"
    strength_category: CategoryNameEnum
    strength_achievement_rate: float
    strength_text: str
    improvement_category: CategoryNameEnum
    improvement_achievement_rate: float
    improvement_text: str


# 월별 목표별 달성 현황 (그래프용)
class MonthlyAchievementChartItem(BaseModel):
    month: int  # 예: 1, 2, 3, ...
    achievement_rate: float  # 예: 85.0


class MonthlyAchievementChart(BaseModel):
    category_name: CategoryNameEnum
    monthly_progress: list[MonthlyAchievementChartItem]
