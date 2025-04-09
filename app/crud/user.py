from fastapi import HTTPException
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse, UserUpdate
from app.models.user import User, GenderEnum
from uuid import UUID
from typing import Optional, List


async def read_user_by_id(db: AsyncSession, user_id: UUID) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalars().first()


async def read_user_by_email(db: AsyncSession, email: str) -> Optional[UserResponse]:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def read_users(
    db: AsyncSession,
) -> List[UserResponse]:
    result = await db.execute(select(User))
    return result.scalars().all()


async def create_user(db: AsyncSession, user_data: UserCreate) -> UserResponse:

    if await read_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="이미 존재하는 이메일입니다.")

    db_user = User(
        email=user_data.email,
        name=user_data.name,
        password=user_data.password,
    )

    await db.add(db_user)
    await db.commit()
    await db.refresh(db_user)

    return db_user


async def update_user(
    db: AsyncSession, user_id: UUID, user_data: UserUpdate
) -> Optional[UserResponse]:
    db_user = await read_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # Pydantic 모델을 딕셔너리로 변환
    update_data = user_data.model_dump()

    # 'sex' 필드가 있으면 실제 Enum 인스턴스로 변환
    if "sex" in update_data and update_data["sex"] is not None:
        gender_map = {
            "M": GenderEnum.MALE,
            "F": GenderEnum.FEMALE,
        }
        update_data["sex"] = gender_map[update_data["sex"]]

    # 모델 속성 업데이트
    for key, value in update_data.items():
        setattr(db_user, key, value)

    await db.commit()
    await db.refresh(db_user)

    return db_user


async def delete_user(db: AsyncSession, user_id: UUID) -> bool:

    db_user = await read_user_by_id(db, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="사용자를 찾을 수 없습니다.")

    # 사용자 삭제
    delete_statement = delete(User).where(User.id == user_id)

    await db.execute(delete_statement)
    await db.commit()

    return True
