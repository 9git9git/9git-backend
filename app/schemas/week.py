from app.schemas.base import BaseModel
from uuid import UUID
from app.enum.week import WeekdayEnum


class WeekCreate(BaseModel):
    weekName: WeekdayEnum


class WeekResponse(BaseModel):
    id: UUID
    week_name: WeekdayEnum


class WeekUpdate(BaseModel):
    weekName: WeekdayEnum
