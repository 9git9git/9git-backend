from app.schemas.base import BaseModel
from uuid import UUID
from datetime import datetime


class MemoCreate(BaseModel):
    title: str
    content: str
    startDate: datetime
    endDate: datetime


class MemoResponse(BaseModel):
    id: UUID
    category_id: UUID
    title: str
    content: str
    start_date: datetime
    end_date: datetime


class MemoUpdate(BaseModel):
    title: str
    content: str
    startDate: datetime
    endDate: datetime
