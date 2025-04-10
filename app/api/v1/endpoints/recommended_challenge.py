# routers/recommended_challenge.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List

from app.db.session import get_db
from app.enum.category import CategoryNameEnum

from app.schemas.base import ResponseBase
from app.schemas.recommended_challenge import (
    RecommendedChallengeCreate,
    RecommendedChallengeUpdate,
    RecommendedChallengeResponse,
)
from app.services.recommended_challenge import (
    select_recommended_challenge_by_id,
    select_recommended_challenges,
    register_recommended_challenge,
    update_recommended_challenge_by_id,
    delete_recommended_challenge_by_id,
)


router = APIRouter()


# 전체 조회 (user_id + category_name)
@router.get(
    "/user/{user_id}/category/{category_name}",
    response_model=ResponseBase[List[RecommendedChallengeResponse]],
)
async def get_recommended_challenges(
    user_id: UUID,
    category_name: str,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[RecommendedChallengeResponse]]:
    try:
        challenges = await select_recommended_challenges(db, user_id, category_name)
        return ResponseBase(status_code=200, data=challenges)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))


# ✅ 단일 조회 (ID 기준)
@router.get(
    "/{challenge_id}",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def get_recommended_challenge_by_id(
    challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        challenge = await select_recommended_challenge_by_id(db, challenge_id)
        if not challenge:
            return ResponseBase(status_code=404, error="추천 과제를 찾을 수 없습니다.")
        return ResponseBase(status_code=200, data=challenge)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))
    
    

# 생성
@router.post(
    "/",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def post_recommended_challenge(
    challenge_data: RecommendedChallengeCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        challenge = await register_recommended_challenge(db, challenge_data)
        return ResponseBase(status_code=201, data=challenge)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))




# 수정
@router.put(
    "/{challenge_id}",
    response_model=ResponseBase[RecommendedChallengeResponse],
)
async def put_recommended_challenge(
    challenge_id: UUID,
    challenge_data: RecommendedChallengeUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[RecommendedChallengeResponse]:
    try:
        challenge = await update_recommended_challenge_by_id(
            db, challenge_id, challenge_data
        )
        return ResponseBase(status_code=200, data=challenge)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))
    
    
# 삭제
@router.delete(
    "/{challenge_id}",
    response_model=ResponseBase[bool],
)
async def delete_recommended_challenge(
    challenge_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_recommended_challenge_by_id(db, challenge_id)
        return ResponseBase(status_code=200, data=result)
    except Exception as e:
        return ResponseBase(status_code=500, error=str(e))