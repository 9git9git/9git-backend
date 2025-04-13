from app.crud.category import (
    create_category,
    read_categories,
    read_category_by_name,
    read_category_by_id,
    update_category,
    delete_category,
)
from app.schemas.category import CategoryCreate, CategoryUpdate, CategoryResponse
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from typing import List
from uuid import UUID


async def add_category(
    db: AsyncSession, category_data: CategoryCreate
) -> CategoryResponse:
    existing = await read_category_by_name(db, category_data.category_name)
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 카테고리입니다.")

    category = await create_category(db, category_data)
    return category


async def select_categories(db: AsyncSession) -> List[CategoryResponse]:
    return await read_categories(db)


async def select_category_by_name(
    db: AsyncSession, category_name: str
) -> CategoryResponse:
    category = await read_category_by_name(db, category_name)
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    return category


async def select_category_by_id(
    db: AsyncSession, category_id: UUID
) -> CategoryResponse:
    category = await read_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
    return category


async def update_category_by_id(
    db: AsyncSession, category_id: UUID, category_data: CategoryUpdate
) -> CategoryResponse:
    category = await read_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    updated_category = await update_category(db, category_id, category_data)
    return updated_category


async def delete_category_by_id(db: AsyncSession, category_id: UUID) -> bool:
    category = await read_category_by_id(db, category_id)
    if not category:
        raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")

    return await delete_category(db, category_id)
