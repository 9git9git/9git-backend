from uuid import UUID
from decimal import Decimal
from typing import Optional
from app.schemas.base import BaseModel
from app.models.category import CategoryNameEnum  # 모델에서 정의된 Enum 사용


# 👉 생성 요청용 스키마 (프론트 → 백)
# ※ progress_rate는 서버에서 자동 계산됨
class CategoryProgressCreate(BaseModel):
    user_id: UUID
    category_name: CategoryNameEnum
    total_goal: int
    completed_goal: int


# 👉 조회 응답용 스키마 (백 → 프론트)
class CategoryProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_name: CategoryNameEnum
    total_goal: int
    completed_goal: int
    progress_rate: Decimal  # 진행률은 계산된 값


# 👉 수정 요청용 스키마 (프론트 → 백)
class CategoryProgressUpdate(BaseModel):
    total_goal: Optional[int]
    completed_goal: Optional[int]
