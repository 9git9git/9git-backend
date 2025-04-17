from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.character import CharacterCreate, CharacterUpdate
from app.models.user import Character
from uuid import UUID
from typing import Optional, List


async def create_character(
    db: AsyncSession, character_data: CharacterCreate
) -> Character:
    db_character = Character(
        character_name=character_data.character_name,
        image_link=character_data.image_link,
    )

    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)

    return db_character


async def read_characters(db: AsyncSession) -> List[Character]:
    result = await db.execute(select(Character))
    characters = result.scalars().all()
    return characters


async def read_character_by_id(
    db: AsyncSession, character_id: UUID
) -> Optional[Character]:
    result = await db.execute(select(Character).where(Character.id == character_id))
    character = result.scalars().first()
    return character


async def read_character_by_name(
    db: AsyncSession, character_name: str
) -> Optional[Character]:
    result = await db.execute(
        select(Character).where(Character.character_name == character_name)
    )
    character = result.scalars().first()
    return character


async def update_character(
    db: AsyncSession, character_id: UUID, character_data: CharacterUpdate
) -> Optional[Character]:
    result = await db.execute(select(Character).where(Character.id == character_id))
    db_character = result.scalars().first()
    if not db_character:
        return None

    update_data = character_data.model_dump()
    for key, value in update_data.items():
        setattr(db_character, key, value)

    await db.commit()
    await db.refresh(db_character)

    return db_character


async def delete_character(db: AsyncSession, character_id: UUID) -> bool:
    try:
        delete_statement = delete(Character).where(Character.id == character_id)
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
