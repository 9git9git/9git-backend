from uuid import UUID
from datetime import date
from typing import Optional
from app.schemas.base import BaseModel


# 요청: 할 일 생성용
class TodoCreate(BaseModel):
    weekId: Optional[UUID] = None
    content: str
    startDate: date
    endDate: date
    isCompleted: bool = False
    isRepeat: bool = False


# 응답: 할 일 조회용
class TodoResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    week_id: UUID
    content: str
    start_date: date
    end_date: date
    is_completed: bool
    is_repeat: bool


# 요청: 할 일 수정용 (전부 Optional)
class TodoUpdate(BaseModel):
    content: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    isCompleted: Optional[bool] = None
    isRepeat: Optional[bool] = None
    categoryId: Optional[UUID] = None
    weekId: Optional[UUID] = None
