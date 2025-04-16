from fastapi import HTTPException, status
from app.crud.user_character import (
    create_user_character,
    read_user_character_by_user_id_and_character_id,
    read_user_character_by_user_id,
    read_user_character_by_character_id,
    delete_user_character,
    read_user_characters,
    update_user_character,
)
from app.schemas.user_character import (
    UserCharacterCreate,
    UserCharacterResponse,
    UserCharacterUpdate,
)
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID


async def add_user_character(
    db: AsyncSession, user_character_data: UserCharacterCreate
) -> UserCharacterResponse:
    # 중복 여부 확인
    existing = await read_user_character_by_user_id_and_character_id(
        db,
        user_id=user_character_data.user_id,
        character_id=user_character_data.character_id,
    )

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="이미 수집한 캐릭터입니다."
        )

    # 중복 없으면 생성 진행
    return await create_user_character(db, user_character_data)


async def select_user_characters(
    db: AsyncSession,
) -> List[UserCharacterResponse]:
    return await read_user_characters(db)


async def select_user_character_by_character_id(
    db: AsyncSession, character_id: UUID
) -> List[UserCharacterResponse]:
    return await read_user_character_by_character_id(db, character_id)


async def select_user_character_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[UserCharacterResponse]:
    return await read_user_character_by_user_id(db, user_id)


async def select_user_character_by_user_id_and_character_id(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> UserCharacterResponse:
    return await read_user_character_by_user_id_and_character_id(
        db, user_id, character_id
    )


async def update_user_character_by_user_id_and_character_id(
    db: AsyncSession,
    user_id: UUID,
    character_id: UUID,
    user_character_data: UserCharacterUpdate,
) -> UserCharacterResponse:
    return await update_user_character(db, user_id, character_id, user_character_data)


async def delete_user_character_by_user_id_and_character_id(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> bool:
    return await delete_user_character(db, user_id, character_id)
