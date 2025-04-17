from datetime import datetime
from typing import Optional
from app.schemas.category import CategoryResponse
from pydantic import BaseModel, Field
from uuid import UUID
from typing import Optional
from datetime import datetime


class StorageCreate(BaseModel):
    title: Optional[str] = None
    created_at: datetime


class StorageResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime
    category: Optional[CategoryResponse] = None


class StorageUpdate(BaseModel):
    title: str
