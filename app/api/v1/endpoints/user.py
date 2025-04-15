from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.user import UserResponse, UserUpdate, UserInformationResponse
from app.schemas.base import ResponseBase
from app.services.user import (
    select_users,
    select_user_by_id,
    select_user_by_email,
    update_user_by_id,
    delete_user_by_id,
)
from app.db.session import get_db
from typing import List
from uuid import UUID

router = APIRouter()


@router.get("/", response_model=ResponseBase[List[UserResponse]])
async def get_users(
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[UserResponse]]:
    try:
        users = await select_users(db)
        return ResponseBase(status_code=status.HTTP_200_OK, data=users)
    # crud 에서 발생시키는 HTTPException 에러를 캐치하기 위함
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    # 일반 예외 처리 ex) db 끊김
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 프론트엔드에서 사용할 유저 정보 조회 API
@router.get("/{user_id}", response_model=ResponseBase[UserInformationResponse])
async def get_user_by_id(user_id: UUID, db: AsyncSession = Depends(get_db)):
    try:
        user_info = await select_user_by_id(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user_info)
    except HTTPException as e:
        raise ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/emails/{email}", response_model=ResponseBase[UserResponse])
async def get_user_by_email(
    email: str,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserResponse]:
    try:
        user = await select_user_by_email(db, email)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{user_id}", response_model=ResponseBase[UserResponse])
async def put_user_by_id(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[UserResponse]:
    try:
        user = await update_user_by_id(db, user_id, user_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=user)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{user_id}", response_model=ResponseBase[bool])
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_user_by_id(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
