from typing import List, Optional
from uuid import UUID
from datetime import date
from decimal import Decimal
from app.schemas.base import BaseModel
from app.schemas.category import CategoryResponse


class ProgressCreate(BaseModel):
    categoryId: UUID


class ProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    progress_rate: Decimal
    category: Optional[CategoryResponse] = None


class TodayProgressResponse(BaseModel):
    totalProgressRate: Decimal
    cheerUpMessage: str
    categoryProgresses: List[ProgressResponse]


class ProgressUpdate(BaseModel):
    progressRate: Decimal | None = None
