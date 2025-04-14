from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime
from typing import List
from app.models.category import Memo
from app.schemas.memo import MemoCreate, MemoResponse, MemoUpdate
from app.utils.to_snake_case import camel_to_snake


async def create_memo(
    db: AsyncSession, user_id: UUID, category_id: UUID, memo: MemoCreate
) -> MemoResponse:

    db_memo = Memo(
        user_id=user_id,
        category_id=category_id,
        title=memo.title,
        content=memo.content,
        start_date=memo.startDate,
        end_date=memo.endDate,
    )

    db.add(db_memo)
    await db.commit()
    await db.refresh(db_memo)
    return db_memo


async def read_memos(db: AsyncSession, user_id: UUID) -> List[MemoResponse]:
    db_memo = await db.execute(select(Memo).where(Memo.user_id == user_id))
    return db_memo.scalars().all()


async def read_memo_by_id(
    db: AsyncSession, user_id: UUID, memo_id: UUID
) -> MemoResponse:
    db_memo = await db.execute(
        select(Memo).where(Memo.id == memo_id, Memo.user_id == user_id)
    )
    return db_memo.scalars().first()


async def read_memos_by_date(
    db: AsyncSession, user_id: UUID, date: datetime
) -> List[MemoResponse]:
    db_memo = await db.execute(
        select(Memo).where(
            Memo.user_id == user_id, Memo.start_date <= date, date <= Memo.end_date
        )
    )
    return db_memo.scalars().all()


async def read_memos_by_period(
    db: AsyncSession, user_id: UUID, start_date: datetime, end_date: datetime
) -> List[MemoResponse]:
    db_memo = await db.execute(
        select(Memo).where(
            Memo.user_id == user_id,
            Memo.start_date >= start_date,
            Memo.end_date <= end_date,
        )
    )
    return db_memo.scalars().all()


async def read_memos_by_category_id(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[MemoResponse]:
    db_memo = await db.execute(
        select(Memo).where(Memo.user_id == user_id, Memo.category_id == category_id)
    )
    return db_memo.scalars().all()


async def read_memos_by_period_and_category_id(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    start_date: datetime,
    end_date: datetime,
) -> List[MemoResponse]:
    db_memo = await db.execute(
        select(Memo).where(
            Memo.user_id == user_id,
            Memo.category_id == category_id,
            Memo.start_date >= start_date,
            Memo.end_date <= end_date,
        )
    )
    return db_memo.scalars().all()


async def update_memo(
    db: AsyncSession, user_id: UUID, memo_id: UUID, memo_data: MemoUpdate
) -> MemoResponse:
    db_memo = await read_memo_by_id(db, user_id, memo_id)

    update_data = memo_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(db_memo, snake_key, value)

    await db.commit()
    await db.refresh(db_memo)
    return db_memo


async def delete_memo(db: AsyncSession, user_id: UUID, memo_id: UUID) -> bool:
    delete_statement = delete(Memo).where(Memo.id == memo_id, Memo.user_id == user_id)

    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
