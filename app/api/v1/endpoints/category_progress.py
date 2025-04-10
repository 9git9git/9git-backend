from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.schemas.category_progress import (
    CategoryProgressCreate,
    CategoryProgressUpdate,
    CategoryProgressResponse,
)
from app.schemas.base import ResponseBase
from app.services.category_progress import (
    select_category_progress_by_id,
    select_category_progresses_by_user_id,
    register_category_progress,
    update_category_progress_by_id,
    delete_category_progress_by_id,
)

router = APIRouter(prefix="/category-progresses", tags=["CategoryProgress"])


# 특정 사용자(user_id)의 전체 진행 정보 조회
@router.get(
    "/user/{user_id}", response_model=ResponseBase[List[CategoryProgressResponse]]
)
async def get_progresses_by_user_id(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[CategoryProgressResponse]]:
    try:
        progresses = await select_category_progresses_by_user_id(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=progresses)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# ID 기준 단일 조회
@router.get("/{progress_id}", response_model=ResponseBase[CategoryProgressResponse])
async def get_progress_by_id(
    progress_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryProgressResponse]:
    try:
        progress = await select_category_progress_by_id(db, progress_id)
        if not progress:
            return ResponseBase(
                status_code=404, error="카테고리 진행 정보를 찾을 수 없습니다."
            )
        return ResponseBase(status_code=200, data=progress)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 생성 (진행률은 서버에서 계산)
@router.post("/", response_model=ResponseBase[CategoryProgressResponse])
async def post_progress(
    progress_data: CategoryProgressCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryProgressResponse]:
    try:
        progress = await register_category_progress(db, progress_data)
        return ResponseBase(status_code=201, data=progress)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 수정 (변경된 목표/완료 수 기준으로 진행률 재계산)
@router.put("/{progress_id}", response_model=ResponseBase[CategoryProgressResponse])
async def put_progress_by_id(
    progress_id: UUID,
    progress_data: CategoryProgressUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryProgressResponse]:
    try:
        progress = await update_category_progress_by_id(db, progress_id, progress_data)
        return ResponseBase(status_code=200, data=progress)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# 삭제
@router.delete("/{progress_id}", response_model=ResponseBase[bool])
async def delete_progress_by_id(
    progress_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_category_progress_by_id(db, progress_id)
        return ResponseBase(status_code=200, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))
