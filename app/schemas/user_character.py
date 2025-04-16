from uuid import UUID
from app.schemas.base import BaseModel
from app.schemas.character import CharacterResponse
from app.schemas.user import UserResponse
from typing import Optional


class UserCharacterCreate(BaseModel):
    user_id: UUID
    character_id: UUID


class UserCharacterResponse(BaseModel):
    id: UUID
    user_id: UUID
    character_id: UUID
    character: Optional[CharacterResponse] = None
    # user: Optional[UserResponse] = None 응답때메 없애버리기


class UserCharacterUpdate(BaseModel):
    user_id: UUID
    character_id: UUID
