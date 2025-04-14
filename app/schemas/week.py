from app.schemas.base import BaseModel
from uuid import UUID


class WeekCreate(BaseModel):
    weekName: str


class WeekResponse(BaseModel):
    id: UUID
    week_name: str


class WeekUpdate(BaseModel):
    weekName: str
