from pydantic import BaseModel
from uuid import UUID
from app.enum.category import CategoryNameEnum, CategoryColorEnum
from typing import Optional


# 생성용
class CategoryCreate(BaseModel):
    category_name: CategoryNameEnum
    category_color: CategoryColorEnum


# 응답용
class CategoryResponse(BaseModel):
    id: UUID
    category_name: CategoryNameEnum
    category_color: CategoryColorEnum

    class Config:
        orm_mode = True


# 수정용
class CategoryUpdate(BaseModel):
    category_name: Optional[CategoryNameEnum] = None
    catecategory_color: Optional[CategoryColorEnum] = None
