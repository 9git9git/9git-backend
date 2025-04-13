from app.schemas.memo import MemoCreate, MemoResponse, MemoUpdate
from app.crud.memo import (
    create_memo,
    read_memo_by_id,
    read_memos_by_date,
    read_memos_by_month,
    update_memo,
    delete_memo,
)
from typing import List, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime, timedelta

# TODO(Gideok Kim): 일정에서 보일 메모 데이터 캐싱을 어디에 해둘지에 따라 로직 변경 필요.
# 현재 구조는 모든 유저가 이곳에 캐싱되기 때문에 좋지 않음.
memo_cache: Dict[str, List[MemoResponse]] = {}


async def select_today_memos_service(
    db: AsyncSession, user_id: UUID
) -> List[MemoResponse]:
    today = datetime.now().date()
    return await read_memos_by_date(db, user_id, today)


async def select_month_memos_service(
    db: AsyncSession, user_id: UUID, year: int, month: int
) -> List[MemoResponse]:
    cache_key = f"{user_id}_{year}_{month}"
    if cache_key in memo_cache:
        return memo_cache[cache_key]

    start_date = datetime(year, month, 1)
    end_date = datetime(year, month + 1, 1) - timedelta(days=1)
    db_memos = await read_memos_by_month(db, user_id, start_date, end_date)
    memo_cache[cache_key] = db_memos
    return db_memos


async def select_month_memos_by_category_id_service(
    db: AsyncSession, user_id: UUID, category_id: UUID, year: int, month: int
) -> List[MemoResponse]:
    db_memos = await select_month_memos_service(db, user_id, year, month)

    return [memo for memo in db_memos if memo.category_id == category_id]


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
