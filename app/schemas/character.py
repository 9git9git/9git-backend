from app.schemas.base import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional


class CharacterCreate(BaseModel):
    character_name: str
    image_link: str


class CharacterResponse(BaseModel):
    id: UUID
    character_name: str
    level: int
    image_link: str
    created_at: datetime
    updated_at: datetime
    is_collected: Optional[bool] = None
    collected_date: Optional[datetime] = None


class CharacterUpdate(BaseModel):
    character_name: str
    image_link: str
