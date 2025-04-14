from http.client import HTTPException
from fastapi import APIRouter, Depends
from app.schemas.base import ResponseBase
from app.schemas.storage import StorageCreate, StorageResponse, StorageUpdate
from app.services.storage import (
    add_storage,
    select_storage_by_id,
    select_storages,
    update_storage_service,
    delete_storage_service,
)
from app.db.session import get_db
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from fastapi import status

router = APIRouter()


@router.get("/", response_model=ResponseBase[List[StorageResponse]])
async def get_storages(
    user_id: UUID,
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[StorageResponse]]:
    try:
        storages = await select_storages(db, user_id, category_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=storages)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{storage_id}", response_model=ResponseBase[StorageResponse])
async def get_storage_by_id(
    user_id: UUID,
    category_id: UUID,
    storage_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[StorageResponse]:
    try:
        storage = await select_storage_by_id(db, user_id, category_id, storage_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=storage)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/", response_model=ResponseBase[StorageResponse])
async def post_storage(
    user_id: UUID,
    category_id: UUID,
    storage_data: StorageCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[StorageResponse]:
    try:
        storage = await add_storage(db, user_id, category_id, storage_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=storage)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{storage_id}", response_model=ResponseBase[StorageResponse])
async def put_storage(
    user_id: UUID,
    category_id: UUID,
    storage_id: UUID,
    storage_data: StorageUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[StorageResponse]:
    try:
        storage = await update_storage_service(
            db, user_id, category_id, storage_id, storage_data
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=storage)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{storage_id}", response_model=ResponseBase[bool])
async def delete_storage(
    user_id: UUID,
    category_id: UUID,
    storage_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        is_deleted = await delete_storage_service(db, user_id, category_id, storage_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=is_deleted)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
