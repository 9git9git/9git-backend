from typing import List, Optional
from uuid import UUID
from app.schemas.storage import StorageCreate, StorageResponse, StorageUpdate
from app.models.chat import Storage
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.orm import selectinload


async def create_storage(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    storage_data: StorageCreate,
) -> StorageResponse:
    title = (
        storage_data.title
        or f"[{storage_data.created_at.strftime('%Y-%m-%d')}] New Chat"
    )

    db_storage = Storage(
        user_id=user_id,
        category_id=category_id,
        title=title,
        created_at=storage_data.created_at,
    )

    db.add(db_storage)
    await db.commit()
    await db.refresh(db_storage)

    return StorageResponse(
        id=db_storage.id,
        title=db_storage.title,
        created_at=db_storage.created_at,
        updated_at=db_storage.updated_at,
        category=None,
    )


async def read_storages(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[StorageResponse]:
    result = await db.execute(
        select(Storage)
        .options(selectinload(Storage.category))
        .where(Storage.user_id == user_id, Storage.category_id == category_id)
    )
    return result.scalars().all()


async def read_storage_by_id(
    db: AsyncSession, user_id: UUID, category_id: UUID, storage_id: UUID
) -> Optional[StorageResponse]:
    result = await db.execute(
        select(Storage)
        .options(selectinload(Storage.category))
        .where(
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

    try:
        await db.execute(delete_statement)
        await db.commit()

    except Exception as e:
        await db.rollback()
        raise e

    return True
