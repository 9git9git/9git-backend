from app.schemas.auth import LoginRequest, LoginResponse, TokenPayload
from app.utils.hashed import verify_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.user import read_user_by_email
from fastapi import HTTPException
from jose import jwt
from datetime import datetime, timedelta
from typing import Optional
from app.core.config import settings
from fastapi import status


async def login_service(db: AsyncSession, login_request: LoginRequest):
    user = await read_user_by_email(db, login_request.email)

    verified = verify_password(login_request.password, user.password)
    if not user:
        raise HTTPException(status_code=401, detail="존재하지 않는 이메일입니다.")
    if not verified:
        raise HTTPException(status_code=401, detail="비밀번호가 일치하지 않습니다.")

    # JWT 토큰 생성
    access_token = create_access_token(
        data={"sub": str(user.id), "email": user.email},
    )

    # 응답 객체 생성
    response = LoginResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        access_token=access_token,
        token_type="bearer",
    )

    return response


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:

    to_encode = {
        **data,
        "exp": datetime.now() + (expires_delta or timedelta(minutes=60 * 24)),
    }

    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def decode_token(token: str) -> Optional[TokenPayload]:
    try:
        payload_dict = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])

        return TokenPayload(**payload_dict)
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰 형식입니다.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"토큰 검증 중 오류가 발생했습니다. {e}",
        )


async def verify_token_service(token: str) -> Optional[TokenPayload]:
    """
    JWT 토큰의 유효성을 검증하고 payload를 반환합니다.
    유효하지 않은 토큰인 경우 HTTP 401 예외를 발생시킵니다.

    Args:
        db: 데이터베이스 세션
        token: 검증할 JWT 토큰

    Returns:
        dict: 토큰의 payload

    Raises:
        HTTPException: 토큰이 유효하지 않은 경우 (401 Unauthorized)
    """

    payload = decode_token(token)

    if not payload:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰 형식입니다.",
        )

    # 만료 시간 검증
    if payload.exp < datetime.now().timestamp():
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="만료된 토큰입니다."
        )

    # TokenPayload 객체를 dict로 변환하여 반환
    return payload
