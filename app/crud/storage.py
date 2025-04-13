from typing import List, Optional
from uuid import UUID
from app.schemas.storage import StorageCreate, StorageResponse, StorageUpdate
from app.models.chat import Storage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete


async def create_storage(
    db: AsyncSession, storage_data: StorageCreate
) -> StorageResponse:
    db_storage = Storage(
        title=storage_data.title,
    )

    db.add(db_storage)
    await db.commit()
    await db.refresh(db_storage)

    return db_storage


async def read_storages(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[StorageResponse]:
    result = await db.execute(
        select(Storage).where(
            Storage.user_id == user_id, Storage.category_id == category_id
        )
    )
    return result.scalars().all()


async def read_storage_by_id(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_id: UUID
) -> Optional[StorageResponse]:
    result = await db.execute(
        select(Storage).where(
            Storage.user_id == user_id,
            Storage.category_id == category_id,
            Storage.id == storage_id,
        )
    )
    return result.scalars().first()


async def update_storage(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    storage_id: UUID,
    storage_data: StorageUpdate,
) -> Optional[StorageResponse]:
    db_storage = await read_storage_by_id(db, user_id, category_id, storage_id)

    db_storage.title = storage_data.title
    await db.commit()
    await db.refresh(db_storage)

    return db_storage


async def delete_storage(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_id: UUID
) -> bool:

    delete_statement = delete(Storage).where(
        Storage.user_id == user_id,
        Storage.category_id == category_id,
        Storage.id == storage_id,
    )

    await db.execute(delete_statement)
    await db.commit()

    return True
