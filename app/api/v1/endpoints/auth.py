from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserCreate, UserResponse
from app.services.user import register_user
from app.db.session import get_db
from loguru import logger

router = APIRouter()


@router.post("/register", response_model=UserResponse)
async def post_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db),
) -> UserResponse:
    logger.info(f"user_data: {user_data}")
    try:
        return await register_user(db, user_data)

    except Exception as e:

        raise HTTPException(status_code=500, detail=str(e))
