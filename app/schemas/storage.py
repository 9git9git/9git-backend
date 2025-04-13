from pydantic import BaseModel
from uuid import UUID


class StorageCreate(BaseModel):
    id: UUID
    title: str


class StorageResponse(BaseModel):
    id: UUID
    title: str


class StorageUpdate(BaseModel):
    title: str
