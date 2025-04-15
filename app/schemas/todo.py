from uuid import UUID
from datetime import date
from typing import List, Optional
from app.schemas.base import BaseModel
from app.schemas.week import WeekCreate, WeekResponse
from app.schemas.category import CategoryResponse


# 요청: 할 일 생성용
class TodoCreate(BaseModel):
    content: str
    startDate: date
    endDate: date
    isCompleted: bool = False
    isRepeat: bool = False
    weeks: Optional[List[WeekCreate]] = None


# 응답: 할 일 조회용
class TodoResponse(BaseModel):
    id: UUID
    user_id: UUID
    category_id: UUID
    content: str
    start_date: date
    end_date: date
    is_completed: bool
    is_repeat: bool
    weeks: Optional[List[WeekResponse]] = None
    category: Optional[CategoryResponse] = None


# 요청: 할 일 수정용 (전부 Optional)
class TodoUpdate(BaseModel):
    content: Optional[str] = None
    startDate: Optional[date] = None
    endDate: Optional[date] = None
    isCompleted: Optional[bool] = None
    isRepeat: Optional[bool] = None
    weeks: Optional[List[WeekResponse]] = None
