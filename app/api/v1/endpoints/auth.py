from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.schemas.base import ResponseBase
from app.services.user import register_user
from app.db.session import get_db
from loguru import logger

router = APIRouter()


@router.post("/register", response_model=ResponseBase[UserResponse])
async def post_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserResponse]:
    logger.info(f"user_data: {user_data}")
    try:
        user = await register_user(db, user_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=user)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
