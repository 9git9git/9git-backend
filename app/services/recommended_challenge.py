from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from decimal import Decimal
from typing import List, Optional

from app.crud.recommended_challenge import (
    create_recommended_challenge,
    read_recommended_challenge_by_id,
    read_recommended_challenge,
    update_recommended_challenge,
    delete_recommended_challenge,
)
from app.schemas.recommended_challenge import RecommendedChallengeCreate, RecommendedChallengeUpdate
from app.models.evaluation import RecommendedChallenge


# ID 기준 단일 조회
async def select_recommended_challenge_by_id(
    db: AsyncSession, challenge_id: UUID
) -> RecommendedChallenge:
    return await read_recommended_challenge_by_id(db, challenge_id)


# user_id & category_name 기준 전체 조회
async def select_recommended_challenges(
    db: AsyncSession, user_id: UUID, category_name: str
) -> List[RecommendedChallenge]:
    return await read_recommended_challenge(db, user_id, category_name)


# 추천 도전 과제 생성
async def register_recommended_challenge(
    db: AsyncSession, challenge_data: RecommendedChallengeCreate
) -> RecommendedChallenge:
    return await create_recommended_challenge(db, challenge_data)


# 추천 도전 과제 수정
async def update_recommended_challenge_by_id(
    db: AsyncSession, challenge_id: UUID, challenge_data: RecommendedChallengeUpdate
) -> RecommendedChallenge:
    return await update_recommended_challenge(
        db, challenge_id, **challenge_data.model_dump(exclude_unset=True)
    )


# 추천 도전 과제 삭제
async def delete_recommended_challenge_by_id(
    db: AsyncSession, challenge_id: UUID
) -> bool:
    return await delete_recommended_challenge(db, challenge_id)
