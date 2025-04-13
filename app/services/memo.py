from app.schemas.memo import MemoCreate, MemoResponse, MemoUpdate
from app.crud.memo import (
    create_memo,
    read_memo_by_id,
    read_memos_by_date,
    read_memos_by_period,
    read_memos_by_period_and_category_id,
    update_memo,
    delete_memo,
)
from typing import List
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timedelta


async def select_today_memos_service(
    db: AsyncSession, user_id: UUID
) -> List[MemoResponse]:
    today = datetime.now().date()
    return await read_memos_by_date(db, user_id, today)


async def select_month_memos_service(
    db: AsyncSession, user_id: UUID, year: int, month: int
) -> List[MemoResponse]:

    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return await read_memos_by_period(db, user_id, start_date, end_date)


async def select_month_memos_by_category_id_service(
    db: AsyncSession, user_id: UUID, category_id: UUID, year: int, month: int
) -> List[MemoResponse]:
    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    return await read_memos_by_period_and_category_id(
        db, user_id, category_id, start_date, end_date
    )


async def add_memo_service(
    db: AsyncSession, user_id: UUID, category_id: UUID, memo: MemoCreate
) -> MemoResponse:
    return await create_memo(db, user_id, category_id, memo)


async def edit_memo_service(
    db: AsyncSession, user_id: UUID, memo_id: UUID, memo: MemoUpdate
) -> MemoResponse:
    try:
        db_memo = await read_memo_by_id(db, user_id, memo_id)
        if not db_memo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="메모를 찾을 수 없습니다."
            )

        return await update_memo(db, user_id, memo_id, memo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 오류가 발생했습니다.",
        ) from e


async def delete_memo_service(db: AsyncSession, user_id: UUID, memo_id: UUID) -> bool:
    try:
        db_memo = await read_memo_by_id(db, user_id, memo_id)
        if not db_memo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="메모를 찾을 수 없습니다."
            )

        return await delete_memo(db, user_id, memo_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 오류가 발생했습니다.",
        ) from e
