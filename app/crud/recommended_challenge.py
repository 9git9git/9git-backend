from uuid import UUID
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy import select, delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.models.evaluation import RecommendedChallenge
from app.schemas.recommended_challenge import (
    RecommendedChallengeCreate,
    RecommendedChallengeUpdate,
    RecommendedChallengeResponse,
)
from app.utils.to_snake_case import camel_to_snake


# 생성
async def create_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    challenge_data: RecommendedChallengeCreate,
) -> RecommendedChallengeResponse:
    db_challenge = RecommendedChallenge(
        user_id=user_id,
        category_id=category_id,
        progress_rate=challenge_data.progressRate,
        challenge_task=challenge_data.challengeTask,
        challenge_duration=challenge_data.challengeDuration,
        challenge_difficulty=challenge_data.challengeDifficulty,
        challenge_suggestion=challenge_data.challengeSuggestion,
    )

    db.add(db_challenge)
    await db.commit()
    await db.refresh(db_challenge)
    return db_challenge


# user_id 기반 전체 조회
async def read_recommended_challenges(
    db: AsyncSession, user_id: UUID
) -> List[RecommendedChallengeResponse]:
    result = await db.execute(
        select(RecommendedChallenge).where(RecommendedChallenge.user_id == user_id)
    )
    return result.scalars().all()


# 단일 조회
async def read_recommended_challenge(
    db: AsyncSession, user_id: UUID, challenge_id: UUID
) -> RecommendedChallengeResponse | None:
    result = await db.execute(
        select(RecommendedChallenge).where(
            RecommendedChallenge.id == challenge_id,
            RecommendedChallenge.user_id == user_id,
        )
    )
    return result.scalars().first()


# 수정
async def update_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
    challenge_data: RecommendedChallengeUpdate,
) -> RecommendedChallengeResponse:
    db_challenge = await read_recommended_challenge(db, user_id, category_id)

    update_data = challenge_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(db_challenge, snake_key, value)

    await db.commit()
    await db.refresh(db_challenge)
    return db_challenge


# 삭제
async def delete_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
) -> bool:
    delete_statement = delete(RecommendedChallenge).where(
        RecommendedChallenge.user_id == user_id,
        RecommendedChallenge.category_id == category_id,
    )
    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
