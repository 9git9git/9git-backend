from datetime import datetime
from typing import Optional
from app.schemas.category import CategoryResponse
from pydantic import BaseModel
from uuid import UUID


class StorageCreate(BaseModel):
    title: str


class StorageResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None


class StorageUpdate(BaseModel):
    title: str
