from app.crud.character import (
    read_characters,
    read_character_by_id,
    create_character,
    update_character,
    delete_character,
)
from app.schemas.character import CharacterResponse, CharacterCreate, CharacterUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID


async def add_character(
    db: AsyncSession, character_data: CharacterCreate
) -> CharacterResponse:
    return await create_character(db, character_data)


async def select_characters(db: AsyncSession) -> List[CharacterResponse]:
    return await read_characters(db)


async def select_character_by_id(
    db: AsyncSession, character_id: UUID
) -> CharacterResponse:
    return await read_character_by_id(db, character_id)


async def update_character_by_id(
    db: AsyncSession, character_id: UUID, character_data: CharacterUpdate
) -> CharacterResponse:
    return await update_character(db, character_id, character_data)


async def delete_character_by_id(db: AsyncSession, character_id: UUID) -> bool:
    return await delete_character(db, character_id)
