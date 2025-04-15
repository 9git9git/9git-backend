from app.schemas.base import ResponseBase
from app.schemas.memo import MemoCreate, MemoResponse, MemoUpdate
from app.services.memo import (
    select_memos_by_period,
    add_memo_service,
    edit_memo_service,
    delete_memo_service,
)
from app.db.session import get_db
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID
from datetime import date

router = APIRouter()


@router.get("/", response_model=ResponseBase[List[MemoResponse]])
async def get_memos_by_period(
    user_id: UUID,
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[MemoResponse]]:
    try:
        memos = await select_memos_by_period(db, user_id, start_date, end_date)
        return ResponseBase(status_code=status.HTTP_200_OK, data=memos)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/", response_model=ResponseBase[MemoResponse])
async def post_memo(
    memo: MemoCreate,
    user_id: UUID,
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MemoResponse]:
    try:
        memo = await add_memo_service(db, user_id, category_id, memo)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=memo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{memo_id}", response_model=ResponseBase[MemoResponse])
async def update_memo(
    user_id: UUID,
    memo_id: UUID,
    memo: MemoUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[MemoResponse]:
    try:
        memo = await edit_memo_service(db, user_id, memo_id, memo)
        return ResponseBase(status_code=status.HTTP_200_OK, data=memo)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{memo_id}", response_model=ResponseBase[bool])
async def delete_memo(
    user_id: UUID,
    memo_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_memo_service(db, user_id, memo_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
