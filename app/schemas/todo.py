from pydantic import BaseModel
from uuid import UUID
from datetime import date
from typing import Optional


class TodoCreate(BaseModel):
    userId: UUID
    categoryId: UUID
    weekId: int
    content: str
    startDate: date
    endDate: date
    isCompleted: bool = False
    isRepeat: bool = False


class TodoResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    week_id: int
    content: str
    start_date: date
    end_date: date
    is_completed: bool
    is_repeat: bool


class TodoUpdate(BaseModel):
    content: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    isCompleted: Optional[bool] = None
    isRepeat: Optional[bool] = None
    categoryId: Optional[UUID] = None
    weekId: Optional[int] = None
