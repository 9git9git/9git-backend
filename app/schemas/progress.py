from pydantic import BaseModel
from uuid import UUID
from datetime import date
from decimal import Decimal


class ProgressCreate(BaseModel):
    user_id: UUID
    category_id: UUID
    start_date: date
    end_date: date


class ProgressUpdate(BaseModel):
    progress_rate: Decimal | None = None
    start_date: date | None = None
    end_date: date | None = None


class ProgressResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    progress_rate: Decimal
    start_date: date
    end_date: date

    class Config:
        orm_mode = True
