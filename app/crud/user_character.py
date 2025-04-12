from app.crud.character import read_character_by_id
from app.crud.user import read_user_by_id
from fastapi import HTTPException
from app.schemas.user_character import (
    UserCharacterCreate,
    UserCharacterResponse,
    UserCharacterUpdate,
)
from app.models.user import UserCharacter
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from sqlalchemy.orm import selectinload


async def create_user_character(
    db: AsyncSession, user_character_data: UserCharacterCreate
) -> UserCharacterResponse:
    if await read_user_character_by_user_id_and_character_id(
        db, user_character_data.userId, user_character_data.characterId
    ):
        raise HTTPException(status_code=400, detail="이미 소유하고 있는 캐릭터입니다.")

    db_user_character = UserCharacter(
        user_id=user_character_data.userId,
        character_id=user_character_data.characterId,
    )

    db.add(db_user_character)
    await db.commit()
    await db.refresh(db_user_character)

    return UserCharacterResponse(
        id=db_user_character.id,
        user_id=db_user_character.user_id,
        character_id=db_user_character.character_id,
        user=None,
        character=None,
    )


async def read_user_characters(
    db: AsyncSession,
) -> List[UserCharacterResponse]:
    result = await db.execute(
        select(UserCharacter).options(
            selectinload(UserCharacter.user), selectinload(UserCharacter.character)
        )
    )
    return result.scalars().all()


async def read_user_character_by_user_id(
    db: AsyncSession, user_id: UUID
) -> List[UserCharacterResponse]:
    result = await db.execute(
        select(UserCharacter)
        .where(UserCharacter.user_id == user_id)
        .options(
            selectinload(UserCharacter.user), selectinload(UserCharacter.character)
        )
    )
    return result.scalars().all()


async def read_user_character_by_character_id(
    db: AsyncSession, character_id: UUID
) -> List[UserCharacterResponse]:
    result = await db.execute(
        select(UserCharacter)
        .where(UserCharacter.character_id == character_id)
        .options(
            selectinload(UserCharacter.user), selectinload(UserCharacter.character)
        )
    )
    return result.scalars().all()


async def read_user_character_by_user_id_and_character_id(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> UserCharacterResponse:

    # 원래 쿼리 실행 (selectinload 포함)
    result = await db.execute(
        select(UserCharacter)
        .where(
            UserCharacter.user_id == user_id, UserCharacter.character_id == character_id
        )
        .options(
            selectinload(UserCharacter.user), selectinload(UserCharacter.character)
        )
    )
    return result.scalars().first()


async def update_user_character(
    db: AsyncSession,
    user_id: UUID,
    character_id: UUID,
    user_character_data: UserCharacterUpdate,
) -> UserCharacterResponse:

    db_user_character = await read_user_character_by_user_id_and_character_id(
        db, user_id, character_id
    )

    if not db_user_character:
        raise HTTPException(
            status_code=404,
            detail=f"유저 ID({user_id})와 캐릭터 ID({character_id})의 조합을 찾을 수 없습니다.",
        )

    existing = await read_user_character_by_user_id_and_character_id(
        db, user_character_data.userId, user_character_data.characterId
    )

    if existing:
        raise HTTPException(
            status_code=400, detail="이미 해당 유저와 캐릭터 조합이 존재합니다."
        )

    user = await read_user_by_id(db, user_character_data.userId)
    if not user:
        raise HTTPException(
            status_code=404,
            detail=f"해당 유저(ID: {user_character_data.userId})를 찾을 수 없습니다.",
        )

    # 해당 character_id가 존재하는지 확인
    character = await read_character_by_id(db, user_character_data.characterId)
    if not character:
        raise HTTPException(
            status_code=404,
            detail=f"해당 캐릭터(ID: {user_character_data.characterId})를 찾을 수 없습니다.",
        )

    # 업데이트 수행
    update_data = user_character_data.model_dump()

    for key, value in update_data.items():
        setattr(db_user_character, key, value)

    await db.commit()
    await db.refresh(db_user_character)

    # Pydantic 모델로 변환하여 반환
    return UserCharacterResponse(
        id=db_user_character.id,
        user_id=db_user_character.user_id,
        character_id=db_user_character.character_id,
        user=None,
        character=None,
    )


async def delete_user_character(
    db: AsyncSession, user_id: UUID, character_id: UUID
) -> bool:
    db_user_character = await read_user_character_by_user_id_and_character_id(
        db, user_id, character_id
    )
    if not db_user_character:
        raise HTTPException(status_code=404, detail="유저 캐릭터를 찾을 수 없습니다.")

    delete_statement = delete(UserCharacter).where(
        UserCharacter.user_id == user_id, UserCharacter.character_id == character_id
    )

    await db.execute(delete_statement)
    await db.commit()

    return True
