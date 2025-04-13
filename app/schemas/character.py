from uuid import UUID
from app.schemas.base import BaseModel


class CharacterCreate(BaseModel):
    characterName: str
    level: int
    imageLink: str


class CharacterResponse(BaseModel):
    id: UUID
    character_name: str
    level: int
    image_link: str


class CharacterUpdate(BaseModel):
    characterName: str
    level: int
    imageLink: str
