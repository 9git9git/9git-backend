from uuid import UUID
from app.schemas.base import BaseModel
from app.enum.chat import RoleEnum  # RoleEnum이 정의된 경로에 맞게 조정 필요


# 생성
class ChatCreate(BaseModel):
    role: RoleEnum
    content: str


# 응답
class ChatResponse(BaseModel):
    id: UUID
    user_id: UUID
    storage_id: UUID
    category_id: UUID
    role: RoleEnum
    content: str


# 수정
class ChatUpdate(BaseModel):
    role: RoleEnum
    content: str
