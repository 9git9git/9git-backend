from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user_character import (
    UserCharacterCreate,
    UserCharacterResponse,
    UserCharacterUpdate,
)
from app.models.user import UserCharacter
from typing import List, Optional
from sqlalchemy.orm import selectinload


async def create_user_character(
    db: AsyncSession, user_character_data: UserCharacterCreate
) -> UserCharacter:
    db_user_character = UserCharacter(
        user_id=user_character_data.user_id,
        character_id=user_character_data.character_id,
    )

    db.add(db_user_character)
    await db.commit()
    await db.refresh(db_user_character)

    # ✅ selectinload로 다시 불러오기
    result = await db.execute(
        select(UserCharacter)
        .where(
            UserCharacter.user_id == db_user_character.user_id,
            UserCharacter.character_id == db_user_character.character_id,
        )
        .options(
            selectinload(UserCharacter.user),
            selectinload(UserCharacter.character),
        )
    )
    full_user_character = result.scalars().first()

    return full_user_character


async def read_user_characters(db: AsyncSession) -> List[UserCharacter]:
    result = await db.execute(
        select(UserCharacter).options(
            selectinload(UserCharacter.user),
            selectinload(UserCharacter.character),
        )
    )
    user_characters = result.scalars().all()
    return user_characters


async def read_user_character_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[UserCharacter]:
    result = await db.execute(
        select(UserCharacter)
        .where(UserCharacter.user_id == user_id)
        .options(
            selectinload(UserCharacter.user),
            selectinload(UserCharacter.character),
        )
    )
    user_characters = result.scalars().all()
    return user_characters


async def read_user_character_by_character_id(
    db: AsyncSession, character_id: UUID
) -> List[UserCharacter]:
    result = await db.execute(
        select(UserCharacter)
        .where(UserCharacter.character_id == character_id)
        .options(
            selectinload(UserCharacter.user),
            selectinload(UserCharacter.character),
        )
    )
    user_characters = result.scalars().all()
    return user_characters


async def read_user_character_by_user_id_and_character_id(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> Optional[UserCharacter]:
    result = await db.execute(
        select(UserCharacter)
        .where(
            UserCharacter.user_id == user_id,
            UserCharacter.character_id == character_id,
        )
        .options(
            selectinload(UserCharacter.user),
            selectinload(UserCharacter.character),
        )
    )
    user_character = result.scalars().first()
    return user_character


async def update_user_character(
    db: AsyncSession,
    user_id: UUID,
    character_id: UUID,
    user_character_data: UserCharacterUpdate,
) -> Optional[UserCharacter]:
    result = await db.execute(
        select(UserCharacter).where(
            UserCharacter.user_id == user_id,
            UserCharacter.character_id == character_id,
        )
    )
    db_user_character = result.scalars().first()
    if not db_user_character:
        return None

    update_data = user_character_data.model_dump()
    for key, value in update_data.items():
        setattr(db_user_character, key, value)

    await db.commit()
    await db.refresh(db_user_character)

    return db_user_character


async def delete_user_character(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> bool:
    try:
        delete_stmt = delete(UserCharacter).where(
            UserCharacter.user_id == user_id,
            UserCharacter.character_id == character_id,
        )
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
