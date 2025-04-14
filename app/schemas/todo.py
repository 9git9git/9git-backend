from uuid import UUID
from datetime import date
from typing import Optional
from app.schemas.base import BaseModel


# 요청: 할 일 생성용
class TodoCreate(BaseModel):
    weekId: int
    content: str
    startDate: date
    endDate: date
    isCompleted: bool = False
    isRepeat: bool = False


# 응답: 할 일 조회용
class TodoResponse(BaseModel):
    id: UUID
    userId: UUID
    categoryId: UUID
    weekId: int
    content: str
    startDate: date
    endDate: date
    isCompleted: bool
    isRepeat: bool


# 요청: 할 일 수정용 (전부 Optional)
class TodoUpdate(BaseModel):
    content: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    isCompleted: Optional[bool] = None
    isRepeat: Optional[bool] = None
    categoryId: Optional[UUID] = None
    weekId: Optional[int] = None
