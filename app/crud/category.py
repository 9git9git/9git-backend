from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from uuid import UUID
from typing import List, Optional
from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate


async def create_category(
    db: AsyncSession, category_data: CategoryCreate
) -> CategoryResponse:
    db_category = Category(
        category_name=category_data.category_name,
        category_color=category_data.category_color,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def read_categories(db: AsyncSession) -> List[CategoryResponse]:
    result = await db.execute(select(Category))
    return result.scalars().all()


async def read_category_by_name(
    db: AsyncSession, category_name: str
) -> Optional[CategoryResponse]:
    result = await db.execute(
        select(Category).where(Category.category_name == category_name)
    )
    return result.scalars().first()


async def read_category_by_id(
    db: AsyncSession, category_id: UUID
) -> Optional[CategoryResponse]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


async def update_category(
    db: AsyncSession, category_id: UUID, category_data: CategoryUpdate
) -> CategoryResponse:
    db_category = await read_category_by_id(db, category_id)

    update_data = category_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(db_category, key, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, category_id: UUID) -> bool:
    delete_statement = delete(Category).where(Category.id == category_id)
    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
