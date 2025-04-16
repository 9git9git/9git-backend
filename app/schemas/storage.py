from datetime import datetime
from pydantic import BaseModel
from uuid import UUID


class StorageCreate(BaseModel):
    title: str


class StorageResponse(BaseModel):
    id: UUID
    title: str
    created_at: datetime
    updated_at: datetime


class StorageUpdate(BaseModel):
    title: str
