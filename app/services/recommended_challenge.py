from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal
from typing import List, Optional
from fastapi import HTTPException, status


from app.schemas.recommended_challenge import (
    RecommendedChallengeCreate,
    RecommendedChallengeUpdate,
    RecommendedChallengeResponse,
)

from app.crud.recommended_challenge import (
    read_recommended_challenge,
    read_recommended_challenges,
    create_recommended_challenge,
    update_recommended_challenge,
    delete_recommended_challenge,
)


# ID 기준 단일 조회
async def select_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    recommended_challenge_id: UUID,
) -> RecommendedChallengeResponse:
    challenge = await read_recommended_challenge(db, user_id, recommended_challenge_id)
    if not challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="추천 도전 과제를 찾을 수 없습니다.",
        )
    return challenge


# 전체 조회
async def select_recommended_challenges(
    db: AsyncSession,
    user_id: UUID,
) -> List[RecommendedChallengeResponse]:
    return await read_recommended_challenges(db, user_id)


# 생성
async def add_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    challenge_data: RecommendedChallengeCreate,
) -> RecommendedChallengeResponse:
    return await create_recommended_challenge(db, user_id, category_id, challenge_data)


# 수정
async def update_recommended_challenge_service(
    db: AsyncSession,
    user_id: UUID,
    recommended_challenge_id: UUID,
    challenge_data: RecommendedChallengeUpdate,
) -> RecommendedChallengeResponse:
    db_challenge = await read_recommended_challenge(
        db, user_id, recommended_challenge_id
    )
    if not db_challenge:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="추천 도전 과제를 찾을 수 없습니다.",
        )

    return await update_recommended_challenge(
        db, user_id, recommended_challenge_id, challenge_data
    )


# 삭제
async def delete_recommended_challenge_service(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
) -> bool:
    try:
        challenge = await read_recommended_challenge(db, user_id, category_id)
        if not challenge:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="추천 도전 과제를 찾을 수 없습니다.",
            )
        return await delete_recommended_challenge(db, user_id, category_id)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="데이터베이스 오류가 발생했습니다.",
        )
