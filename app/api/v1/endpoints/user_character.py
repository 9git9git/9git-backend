from typing import List
from app.schemas.user_character import (
    UserCharacterCreate,
    UserCharacterResponse,
    UserCharacterUpdate,
)
from app.schemas.base import ResponseBase
from app.services.user_character import (
    create_user_character,
    delete_user_character_by_user_id_and_character_id,
    select_user_character_by_character_id,
    select_user_character_by_user_id,
    select_user_character_by_user_id_and_character_id,
    select_user_characters,
    update_user_character_by_user_id_and_character_id,
)
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=ResponseBase[UserCharacterResponse])
async def post_user_character(
    user_character_data: UserCharacterCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserCharacterResponse]:
    try:
        user_character = await create_user_character(db, user_character_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=user_character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/", response_model=ResponseBase[List[UserCharacterResponse]])
async def get_user_characters(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[UserCharacterResponse]]:
    try:
        user_characters = await select_user_characters(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_characters)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{character_id}", response_model=ResponseBase[List[UserCharacterResponse]])
async def get_user_character_by_character_id(
    character_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[UserCharacterResponse]]:
    try:
        user_character = await select_user_character_by_character_id(db, character_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get(
    "/users/{user_id}", response_model=ResponseBase[List[UserCharacterResponse]]
)
async def get_user_character_by_user_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[UserCharacterResponse]]:
    try:
        user_character = await select_user_character_by_user_id(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get(
    "/users/{user_id}/characters/{character_id}",
    response_model=ResponseBase[UserCharacterResponse],
)
async def get_user_character_by_user_id_and_character_id(
    user_id: UUID,
    character_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserCharacterResponse]:
    try:
        user_character = await select_user_character_by_user_id_and_character_id(
            db, user_id, character_id
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put(
    "/users/{user_id}/characters/{character_id}",
    response_model=ResponseBase[UserCharacterResponse],
)
async def update_user_character(
    user_id: UUID,
    character_id: UUID,
    user_character_data: UserCharacterUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserCharacterResponse]:
    try:
        user_character = await update_user_character_by_user_id_and_character_id(
            db, user_id, character_id, user_character_data
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_character)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete(
    "/users/{user_id}/characters/{character_id}", response_model=ResponseBase[bool]
)
async def delete_user_character(
    user_id: UUID,
    character_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_user_character_by_user_id_and_character_id(
            db, user_id, character_id
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
