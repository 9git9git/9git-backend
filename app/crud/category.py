from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate
from app.utils.to_snake_case import camel_to_snake


async def create_category(db: AsyncSession, category_data: CategoryCreate) -> Category:
    db_category = Category(
        category_name=category_data.categoryName,
        category_color=category_data.categoryColor,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def read_categories(db: AsyncSession) -> List[Category]:
    result = await db.execute(select(Category))
    return result.scalars().all()


async def read_category_by_id(
    db: AsyncSession, category_id: UUID
) -> Optional[Category]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalars().first()


async def read_category_by_name(
    db: AsyncSession, category_name: str
) -> Optional[Category]:
    result = await db.execute(
        select(Category).where(Category.category_name == category_name)
    )
    return result.scalars().first()


async def update_category(
    db: AsyncSession, db_category: Category, category_data: CategoryUpdate
) -> Category:
    update_data = category_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(db_category, snake_key, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category


async def delete_category(db: AsyncSession, db_category: Category) -> bool:
    delete_stmt = delete(Category).where(Category.id == db_category.id)
    try:
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
