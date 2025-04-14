from fastapi import HTTPException, status
from app.crud.storage import (
    create_storage,
    read_storages,
    read_storage_by_id,
    update_storage,
    delete_storage,
)
from app.schemas.storage import StorageCreate, StorageResponse, StorageUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List


async def select_storages(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[StorageResponse]:
    return await read_storages(db, user_id, category_id)


async def select_storage_by_id(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_id: UUID
) -> StorageResponse:
    return await read_storage_by_id(db, user_id, category_id, storage_id)


async def add_storage(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_data: StorageCreate
) -> StorageResponse:
    return await create_storage(db, user_id, category_id, storage_data)


async def update_storage_service(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    storage_id: UUID,
    storage_data: StorageUpdate,
) -> StorageResponse:
    db_storage = await read_storage_by_id(db, user_id, category_id, storage_id)
    if not db_storage:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="존재하지 않는 보관함입니다."
        )

    return await update_storage(db, user_id, category_id, storage_id, storage_data)


async def delete_storage_service(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_id: UUID
) -> bool:
    try:
        db_storage = await read_storage_by_id(db, user_id, category_id, storage_id)
        if not db_storage:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="존재하지 않는 보관함입니다.",
            )

        return await delete_storage(db, user_id, category_id, storage_id)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="보관함 삭제 중 오류가 발생했습니다.",
        ) from e
