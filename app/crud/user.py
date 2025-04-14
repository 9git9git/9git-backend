from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User
from uuid import UUID
from typing import Optional, List


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:

    db_user = User(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password,
    )

    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def read_users(
    db: AsyncSession,
) -> List[UserResponse]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def read_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def read_user_by_email(db: AsyncSession, email: str) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def update_user(
    db: AsyncSession, user_id: UUID, user_data: UserUpdate
) -> Optional[UserResponse]:
    db_user = await read_user_by_id(db, user_id)

    # Pydantic 모델을 딕셔너리로 변환
    update_data = user_data.model_dump()

    # 모델 속성 업데이트
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:

    # 사용자 삭제
    delete_statement = delete(User).where(User.id == user_id)

    await db.execute(delete_statement)
    await db.commit()

    return True
