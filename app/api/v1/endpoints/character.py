from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.character import CharacterCreate, CharacterResponse, CharacterUpdate
from app.schemas.base import ResponseBase
from app.services.character import (
    add_character,
    select_characters,
    select_character_by_id,
    delete_character_by_id,
    update_character_by_id,
    get_character_collection,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=ResponseBase[CharacterResponse])
async def post_character(
    character_data: CharacterCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CharacterResponse]:
    try:
        character = await add_character(db, character_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/", response_model=ResponseBase[List[CharacterResponse]])
async def get_characters(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[CharacterResponse]]:
    try:
        characters = await select_characters(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=characters)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{character_id}", response_model=ResponseBase[CharacterResponse])
async def get_character_by_id(
    character_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CharacterResponse]:
    try:
        character = await select_character_by_id(db, character_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{character_id}", response_model=ResponseBase[CharacterResponse])
async def put_character_by_id(
    character_id: UUID,
    character_data: CharacterUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CharacterResponse]:
    try:
        character = await update_character_by_id(db, character_id, character_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{character_id}", response_model=ResponseBase[bool])
async def delete_character(
    character_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_character_by_id(db, character_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 서비스 로직


@router.get("/", response_model=ResponseBase[List[CharacterResponse]])
async def get_user_character_collection(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[CharacterResponse]]:
    try:
        characters = await get_character_collection(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=characters)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            error="캐릭터 도감 조회 중 서버 오류가 발생했습니다.",
        )
