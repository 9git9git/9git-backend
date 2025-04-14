from uuid import UUID
from datetime import date
from decimal import Decimal
from app.schemas.base import BaseModel


class ProgressCreate(BaseModel):
    categoryId: UUID
    startDate: date
    endDate: date


class ProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    progress_rate: Decimal
    start_date: date
    end_date: date


class ProgressUpdate(BaseModel):
    progressRate: Decimal | None = None
    startDate: date | None = None
    endDate: date | None = None
