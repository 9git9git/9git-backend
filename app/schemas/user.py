from pydantic import EmailStr
from enum import Enum
from uuid import UUID
from typing import Optional
from app.schemas.base import BaseModel


class GenderEnum(str, Enum):
    MALE = "M"
    FEMALE = "F"


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
    character_count: Optional[int] = 0


class UserUpdate(BaseModel):
    sex: GenderEnum
    age: int
    job: str
    level: int
    exp: int
    character_count: int


class CharacterResponse(BaseModel):
    id: UUID
    character_name: str
    level: int
    image_link: str


class UserCharacterResponse(BaseModel):
    id: UUID
    user_id: UUID
    character_id: UUID
    character: Optional[CharacterResponse] = None
    user: Optional[UserResponse] = None
