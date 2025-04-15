from app.schemas.base import BaseModel
from uuid import UUID
from pydantic import EmailStr
from typing import Optional
from datetime import datetime


class LoginRequest(BaseModel):
    email: EmailStr
    password: str


class LoginResponse(BaseModel):
    user_id: UUID
    email: EmailStr
    name: str
    access_token: str
    token_type: str


# 토큰 검증 요청 스키마
class TokenVerifyRequest(BaseModel):
    token: str


class TokenPayload(BaseModel):
    sub: str  # 사용자 ID (UUID 문자열)
    email: Optional[str] = None
    exp: int  # 만료 시간 (Unix timestamp)
