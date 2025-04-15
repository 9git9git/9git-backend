from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.schemas.progress import ProgressCreate, ProgressUpdate, ProgressResponse
from app.schemas.base import ResponseBase
from app.services.progress import (
    add_progress,
    select_all_progresses,
    select_progress_by_id,
    update_progress_by_id,
    delete_progress_by_id,
)

router = APIRouter()


@router.post("/", response_model=ResponseBase[ProgressResponse])
async def post_progress(
    user_id: UUID,
    progress_data: ProgressCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ProgressResponse]:
    try:
        progress = await add_progress(db, user_id, progress_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=progress)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/", response_model=ResponseBase[List[ProgressResponse]])
async def get_all_progresses(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[ProgressResponse]]:
    try:
        progresses = await select_all_progresses(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=progresses)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{progress_id}", response_model=ResponseBase[ProgressResponse])
async def get_progress_by_id(
    progress_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ProgressResponse]:
    try:
        progress = await select_progress_by_id(db, progress_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=progress)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{progress_id}", response_model=ResponseBase[ProgressResponse])
async def put_progress_by_id(
    progress_id: UUID,
    progress_data: ProgressUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ProgressResponse]:
    try:
        updated = await update_progress_by_id(db, progress_id, progress_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=updated)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{progress_id}", response_model=ResponseBase[bool])
async def delete_progress(
    progress_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_progress_by_id(db, progress_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
