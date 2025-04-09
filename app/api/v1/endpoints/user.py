from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdate
from app.services.user import (
    select_users,
    select_user_by_id,
    select_user_by_email,
    update_user_by_id,
    delete_user_by_id,
)
from app.db.session import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=List[UserResponse])
async def get_users(
    db: AsyncSession = Depends(get_db),
) -> List[UserResponse]:

    try:
        return await select_users(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{user_id}", response_model=UserResponse)
async def get_user_by_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    try:
        return await select_user_by_id(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/email/{email}", response_model=UserResponse)
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    try:
        return await select_user_by_email(db, email)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{user_id}", response_model=UserResponse)
async def put_user_by_id(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    try:
        return await update_user_by_id(db, user_id, user_data)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{user_id}", response_model=bool)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> bool:
    try:
        return await delete_user_by_id(db, user_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
