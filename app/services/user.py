from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import (
    read_users,
    create_user,
    update_user,
    delete_user,
    read_user_by_id,
    read_user_by_email,
)
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from typing import List
from uuid import UUID
from fastapi import status


async def select_user_by_id(db: AsyncSession, user_id: UUID) -> UserResponse:
    user = await read_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
        )
    return user


async def select_user_by_email(db: AsyncSession, email: str) -> UserResponse:
    return await read_user_by_email(db, email)


async def select_users(db: AsyncSession) -> List[UserResponse]:
    return await read_users(db)


async def register_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    db_user = await read_user_by_email(db, user_data.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="이미 존재하는 이메일입니다.",
        )
    return await create_user(db, user_data)


async def update_user_by_id(
    db: AsyncSession, user_id: UUID, user_data: UserUpdate
) -> UserResponse:
    db_user = await read_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
        )
    return await update_user(db, user_id, user_data)


async def delete_user_by_id(db: AsyncSession, user_id: UUID) -> bool:
    return await delete_user(db, user_id)
