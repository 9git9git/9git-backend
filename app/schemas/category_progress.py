from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.schemas.base import BaseModel
from app.enum.category import CategoryNameEnum


# 생성 스키마
class CategoryProgressCreate(BaseModel):
    user_id: UUID
    category_name: CategoryNameEnum
    total_goal: int
    completed_goal: int


# 응답용 스키마
class CategoryProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_name: CategoryNameEnum
    total_goal: int
    completed_goal: int
    progress_rate: Decimal


# 업데이트용 스키마
class CategoryProgressUpdate(BaseModel):
    total_goal: Optional[int] = None
    completed_goal: Optional[int] = None


# 카테고리 하나당 진행률
class GoalProgressItem(BaseModel):
    category_name: CategoryNameEnum  # 예: 영어, 코딩, 운동
    progress_rate: float  # 예: 75.0


# 카테고리 전체 종합 진행률
class GoalProgressSummary(BaseModel):
    main_message: Optional[str] = None  # "응원 문구" or 대표 목표명
    main_progress_rate: float  # 상단 대표 목표 진행률
    details: list[GoalProgressItem]  # 각 카테고리별 상세 진행률
