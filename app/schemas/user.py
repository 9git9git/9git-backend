from pydantic import EmailStr
from uuid import UUID
from typing import Optional, List
from app.schemas.base import BaseModel
from app.schemas.character import CharacterResponse
from app.enum.user import GenderEnum


class UserCreate(BaseModel):
    email: EmailStr
    name: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: EmailStr
    name: str
    sex: Optional[str] = None
    age: Optional[int] = None
    job: Optional[str] = None
    level: Optional[int] = 1
    exp: Optional[int] = 0
    completed_todo_count: Optional[int] = 0
    character_count: Optional[int] = 0
    characters: Optional[List[CharacterResponse]] = []


class UserUpdate(BaseModel):
    sex: GenderEnum
    age: int
    job: str
    level: int
    exp: int
    character_count: int
