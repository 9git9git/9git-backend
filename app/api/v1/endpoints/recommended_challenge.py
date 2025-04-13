from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db

from app.schemas.base import ResponseBase
from app.schemas.recommended_challenge import (
    RecommendedChallengeCreate,
    RecommendedChallengeUpdate,
    RecommendedChallengeResponse,
)
from app.services.recommended_challenge import (
    select_recommended_challenge,
    select_recommended_challenges,
    add_recommended_challenge,
    update_recommended_challenge_service,
    delete_recommended_challenge_service,
)

router = APIRouter()


# 전체 조회
@router.get(
    "/",
    response_model=ResponseBase[List[RecommendedChallengeResponse]],
)
async def get_recommended_challenges(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[RecommendedChallengeResponse]]:
    try:
        challenges = await select_recommended_challenges(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=challenges)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 단일 조회
@router.get(
    "/{recommended_challenge_id}",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def get_recommended_challenge(
    user_id: UUID,
    recommended_challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        challenge = await select_recommended_challenge(
            db, user_id, recommended_challenge_id
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=challenge)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 생성
@router.post(
    "/",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def post_recommended_challenge(
    user_id: UUID,
    progress_id: UUID,
    category_id: UUID,
    challenge_data: RecommendedChallengeCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        challenge = await add_recommended_challenge(
            db, user_id, progress_id, category_id, challenge_data
        )
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=challenge)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 수정
@router.put(
    "/{recommended_challenge_id}",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def put_recommended_challenge(
    user_id: UUID,
    recommended_challenge_id: UUID,
    challenge_data: RecommendedChallengeUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        updated = await update_recommended_challenge_service(
            db, user_id, recommended_challenge_id, challenge_data
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=updated)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


# 삭제
@router.delete(
    "/{recommended_challenge_id}",
    response_model=ResponseBase[bool],
)
async def delete_recommended_challenge(
    user_id: UUID,
    recommended_challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_recommended_challenge_service(
            db, user_id, recommended_challenge_id
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
