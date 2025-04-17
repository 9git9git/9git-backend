from app.crud.character import (
    read_characters,
    read_character_by_id,
    read_character_by_name,
    create_character,
    update_character,
    delete_character,
)
from app.schemas.character import CharacterResponse, CharacterCreate, CharacterUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from typing import List
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.user import UserCharacter
from app.models.user import Character as CharacterModel


async def add_character(
    db: AsyncSession, character_data: CharacterCreate
) -> CharacterResponse:
    existing = await read_character_by_name(db, character_data.character_name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 캐릭터입니다.",
        )

    return await create_character(db, character_data)


async def select_characters(db: AsyncSession) -> List[CharacterResponse]:
    return await read_characters(db)


async def select_character_by_id(
    db: AsyncSession, character_id: UUID
) -> CharacterResponse:
    character = await read_character_by_id(db, character_id)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="캐릭터를 찾을 수 없습니다.",
        )
    return character


async def update_character_by_id(
    db: AsyncSession, character_id: UUID, character_data: CharacterUpdate
) -> CharacterResponse:
    character = await update_character(db, character_id, character_data)
    if not character:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="캐릭터를 찾을 수 없습니다.",
        )
    return character


async def delete_character_by_id(db: AsyncSession, character_id: UUID) -> bool:
    try:
        character = await read_character_by_id(db, character_id)
        if not character:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="캐릭터를 찾을 수 없습니다.",
            )

        return await delete_character(db, character_id)

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="캐릭터 삭제 중 서버 오류가 발생했습니다.",
        ) from e


# 서비스 로직
from app.models.user import UserCharacter
from uuid import uuid4
from datetime import datetime


async def register_user_character(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> None:
    user_character = UserCharacter(
        id=uuid4(),
        user_id=user_id,
        character_id=character_id,
        collected_at=datetime.utcnow(),
    )
    db.add(user_character)
    await db.commit()


async def get_character_collection(
    db: AsyncSession, user_id: UUID
) -> List[CharacterResponse]:
    try:
        # 1. 전체 캐릭터 조회
        result = await db.execute(select(CharacterModel))
        all_characters = result.scalars().all()

        # 2. 유저 보유 캐릭터 조회 (selectinload 적용)
        user_character_result = await db.execute(
            select(UserCharacter)
            .where(UserCharacter.user_id == user_id)
            .options(
                selectinload(UserCharacter.user),
                selectinload(UserCharacter.character),
            )
        )
        user_characters = user_character_result.scalars().all()

        # 3. 수집 여부 매핑: {character_id: collected_date}
        collected_map = {
            uc.character_id: uc.character.created_at
            for uc in user_characters
            if uc.character is not None
        }

        # 4. 응답 데이터 가공
        result_list = []
        for character in all_characters:
            is_collected = character.id in collected_map
            collected_date = collected_map.get(character.id)
            result_list.append(
                CharacterResponse(
                    id=character.id,
                    character_name=character.character_name,
                    image_link=character.image_link,
                    created_at=character.created_at,
                    updated_at=character.updated_at,
                    is_collected=is_collected,
                    collected_date=collected_date,
                )
            )

        return result_list

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="캐릭터 도감 조회 중 오류가 발생했습니다.",
        ) from e
