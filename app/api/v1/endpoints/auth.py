from fastapi import APIRouter, Depends, status, HTTPException, Response, Cookie
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import LoginRequest, LoginResponse, TokenPayload
from app.schemas.base import ResponseBase
from app.services.user import register_user
from app.services.auth import login_service, verify_token_service
from app.db.session import get_db
from app.core.config import settings

router = APIRouter()


@router.post("/register", response_model=ResponseBase[UserResponse])
async def post_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserResponse]:

    try:
        user = await register_user(db, user_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=user)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/login", response_model=ResponseBase[LoginResponse])
async def login(
    login_request: LoginRequest,
    response: Response,
    db: AsyncSession = Depends(get_db),
):
    try:
        login_response = await login_service(db, login_request)

        # 쿠키에 토큰 설정
        response.set_cookie(
            key="session_token",
            value=login_response.access_token,
            httponly=True,  # JavaScript에서 접근 불가능
            max_age=60 * 60 * 24,  # 1일 (초 단위)
            expires=60 * 60 * 24,  # 1일 (초 단위)
            samesite="none",  # CSRF 보호
            secure=settings.IS_SECURE,  # HTTPS에서만 전송 (프로덕션에서는 True로 설정)
        )

        return ResponseBase(status_code=status.HTTP_200_OK, data=login_response)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/verify-token", response_model=ResponseBase[TokenPayload])
async def verify_token(token: str):
    try:
        payload = await verify_token_service(token)
        return ResponseBase(status_code=status.HTTP_200_OK, data=payload)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
