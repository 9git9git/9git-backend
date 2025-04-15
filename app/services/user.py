from fastapi import HTTPException, status
from app.utils.hashed import get_password_hash
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.crud.user import (
    read_users,
    create_user,
    update_user,
    delete_user,
    read_user_by_id,
    read_user_by_email,
)
from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserUpdate,
    UserInformationResponse,
)
from typing import List
from uuid import UUID
from app.models.user import User


async def select_user_by_id(db: AsyncSession, user_id: UUID) -> UserInformationResponse:
    result = await db.execute(
        select(User).options(selectinload(User.todos)).where(User.id == user_id)
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="사용자를 찾을 수 없습니다."
        )

    completed_todo_count = sum(1 for todo in user.todos if todo.is_completed)

    return UserInformationResponse(
        id=user.id,
        name=user.name,
        email=user.email,
        level=user.level,
        exp=user.exp,
        character_count=user.character_count,
        completed_todo_count=completed_todo_count,
    )


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
    user_data.password = get_password_hash(user_data.password)

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
