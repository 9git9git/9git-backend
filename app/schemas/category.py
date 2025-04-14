from pydantic import BaseModel, ConfigDict
from uuid import UUID
from app.enum.category import CategoryNameEnum, CategoryColorEnum
from typing import Optional


class CategoryCreate(BaseModel):
    categoryName: CategoryNameEnum
    categoryColor: CategoryColorEnum


# 응답용
class CategoryResponse(BaseModel):
    id: UUID
    category_name: CategoryNameEnum
    category_color: CategoryColorEnum

    model_config = ConfigDict(from_attributes=True)


# 수정용
class CategoryUpdate(BaseModel):
    categoryName: Optional[CategoryNameEnum] = None
    categoryColor: Optional[CategoryColorEnum] = None
