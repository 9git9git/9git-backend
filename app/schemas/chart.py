from app.schemas.base import BaseModel
from typing import Literal
from datetime import date


# 일자별 달성률 응답
class DailyAchievementResponse(BaseModel):
    date: date
    english: float
    exercise: float
    coding: float


# 월별 달성률 응답 (optional로 구성 가능)
class MonthlyAchievementResponse(BaseModel):
    month: str  # "2025-01", "2025-02" 형식
    english: float
    exercise: float
    coding: float
