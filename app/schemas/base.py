from pydantic import BaseModel as PydanticBaseModel, ConfigDict
from app.utils.to_camel_case import to_camel_case
from typing import Generic, TypeVar, Optional


class BaseModel(PydanticBaseModel):
    model_config = ConfigDict(
        from_attributes=True,  # ORM 객체를 API 응답으로 사용되는 DTO로 변환 해주게 하는 옵션
        alias_generator=to_camel_case,  # 필드 이름을 camelCase로 변환하는 함수 지정
        populate_by_name=True,
    )


T = TypeVar("T")


class ResponseBase(PydanticBaseModel, Generic[T]):
    status_code: int
    data: Optional[T] = None
    error: Optional[str] = None
