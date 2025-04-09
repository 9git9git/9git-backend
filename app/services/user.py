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


async def select_user_by_id(db: AsyncSession, user_id: UUID) -> UserResponse:
    return await read_user_by_id(db, user_id)


async def select_user_by_email(db: AsyncSession, email: str) -> UserResponse:
    return await read_user_by_email(db, email)


async def select_users(db: AsyncSession) -> List[UserResponse]:
    return await read_users(db)


async def register_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:
    return await create_user(db, user_data)


async def update_user_by_id(
    db: AsyncSession, user_id: UUID, user_data: UserUpdate
) -> UserResponse:
    return await update_user(db, user_id, user_data)


async def delete_user_by_id(db: AsyncSession, user_id: UUID) -> bool:
    return await delete_user(db, user_id)
