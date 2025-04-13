from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.category import CategoryCreate, CategoryResponse, CategoryUpdate
from app.schemas.base import ResponseBase
from app.services.category import (
    add_category,
    select_categories,
    select_category_by_id,
    select_category_by_name,
    update_category_by_id,
    delete_category_by_id,
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.post("/", response_model=ResponseBase[CategoryResponse])
async def post_category(
    category_data: CategoryCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryResponse]:
    try:
        category = await add_category(db, category_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=category)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/", response_model=ResponseBase[List[CategoryResponse]])
async def get_categories(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[CategoryResponse]]:
    try:
        categories = await select_categories(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=categories)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{category_id}", response_model=ResponseBase[CategoryResponse])
async def get_category_by_id(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryResponse]:
    try:
        category = await select_category_by_id(db, category_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=category)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/name/{category_name}", response_model=ResponseBase[CategoryResponse])
async def get_category_by_name(
    category_name: str,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryResponse]:
    try:
        category = await select_category_by_name(db, category_name)
        if not category:
            raise HTTPException(status_code=404, detail="카테고리를 찾을 수 없습니다.")
        return ResponseBase(status_code=status.HTTP_200_OK, data=category)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{category_id}", response_model=ResponseBase[CategoryResponse])
async def put_category_by_id(
    category_id: UUID,
    category_data: CategoryUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[CategoryResponse]:
    try:
        category = await update_category_by_id(db, category_id, category_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=category)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{category_id}", response_model=ResponseBase[bool])
async def delete_category(
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_category_by_id(db, category_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
