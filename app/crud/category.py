from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from app.utils.to_snake_case import camel_to_snake


# ✅ 카테고리 생성
async def create_category(
    db: AsyncSession, category_data: CategoryCreate
) -> CategoryResponse:
    db_category = Category(
        category_name=category_data.categoryName,
        category_color=category_data.categoryColor,
    )
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


# ✅ 전체 카테고리 조회
async def read_categories(db: AsyncSession) -> List[CategoryResponse]:
    result = await db.execute(select(Category))
    categories = result.scalars().all()
    return categories


# ✅ ID로 카테고리 조회
async def read_category_by_id(
    db: AsyncSession, category_id: UUID
) -> Optional[CategoryResponse]:
    result = await db.execute(select(Category).where(Category.id == category_id))
    category = result.scalars().first()
    return category


# ✅ 이름으로 카테고리 조회 (ORM 객체 그대로 반환)
async def read_category_by_name(
    db: AsyncSession, category_name: str
) -> Optional[Category]:
    result = await db.execute(
        select(Category).where(Category.category_name == category_name)
    )
    return result.scalars().first()


# ✅ 카테고리 수정
async def update_category(
    db: AsyncSession, db_category: Category, category_data: CategoryUpdate
) -> CategoryResponse:
    update_data = category_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(db_category, snake_key, value)

    await db.commit()
    await db.refresh(db_category)
    return db_category


# ✅ 카테고리 삭제
async def delete_category(db: AsyncSession, db_category: Category) -> bool:
    delete_stmt = delete(Category).where(Category.id == db_category.id)
    try:
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
