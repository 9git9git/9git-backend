from uuid import UUID
from app.schemas.base import BaseModel
from datetime import datetime
from app.enum.chat import RoleEnum


# 생성
class ChatCreate(BaseModel):
    role: RoleEnum
    content: str
    created_at: datetime


# 응답
class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    storage_id: UUID
    category_id: UUID
    role: RoleEnum
    content: str
    created_at: datetime


class ModelResponse(BaseModel):
    role: RoleEnum = RoleEnum.ASSISTANT
    content: str


class ChatWithModelResponse(BaseModel):
    chat: ChatResponse
    model_response: ModelResponse


# 수정
class ChatUpdate(BaseModel):
    role: RoleEnum
    content: str
