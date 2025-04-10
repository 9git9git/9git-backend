from fastapi import HTTPException
from uuid import UUID
from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate
from app.models.user import Character
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional


async def create_character(
    db: AsyncSession, character_data: CharacterCreate
) -> CharacterResponse:
    if await read_character_by_character_name(db, character_data.characterName):
        raise HTTPException(status_code=400, detail="이미 존재하는 캐릭터 이름입니다.")

    db_character = Character(
        character_name=character_data.characterName,
        level=character_data.level,
        image_link=character_data.imageLink,
    )

    db.add(db_character)
    await db.commit()
    await db.refresh(db_character)

    return db_character


async def read_characters(db: AsyncSession) -> List[CharacterResponse]:
    result = await db.execute(select(Character))
    return result.scalars().all()


async def read_character_by_id(
    db: AsyncSession, character_id: UUID
) -> Optional[CharacterResponse]:
    result = await db.execute(select(Character).where(Character.id == character_id))
    return result.scalars().first()


async def read_character_by_character_name(
    db: AsyncSession, character_name: str
) -> Optional[CharacterResponse]:
    result = await db.execute(
        select(Character).where(Character.character_name == character_name)
    )
    return result.scalars().first()


async def update_character(
    db: AsyncSession, character_id: UUID, character_data: CharacterUpdate
) -> Optional[CharacterResponse]:
    db_character = await read_character_by_id(db, character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    update_data = character_data.model_dump()

    for key, value in update_data.items():
        setattr(db_character, key, value)

    await db.commit()
    await db.refresh(db_character)

    return db_character


async def delete_character(db: AsyncSession, character_id: UUID) -> bool:
    db_character = await read_character_by_id(db, character_id)
    if not db_character:
        raise HTTPException(status_code=404, detail="캐릭터를 찾을 수 없습니다.")

    delete_statement = delete(Character).where(Character.id == character_id)

    await db.execute(delete_statement)
    await db.commit()

    return True
