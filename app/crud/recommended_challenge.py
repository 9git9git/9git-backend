from uuid import UUID
from typing import Optional, List
from fastapi import HTTPException
from sqlalchemy import DECIMAL, select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from app.enum.category import CategoryNameEnum
from app.models.evaluation import RecommendedChallenge
from app.schemas.recommended_challenge import RecommendedChallengeCreate, RecommendedChallengeUpdate


# 생성 
async def create_recommended_challenge(
    db: AsyncSession, challenge_data: RecommendedChallengeCreate
) -> RecommendedChallenge:
    new_challenge = RecommendedChallenge(challenge_data)
    db.add(new_challenge)
    await db.commit()
    await db.refresh(new_challenge)
    return new_challenge


# user_id + category_name 기반 전체 조회
async def read_recommended_challenge(
    db: AsyncSession,
    user_id: UUID,
    category_name: CategoryNameEnum,
) -> List[RecommendedChallenge]:
    result = await db.execute(
        select(RecommendedChallenge).where(
            RecommendedChallenge.user_id == user_id,
            RecommendedChallenge.category_name == category_name,
        )
    )
    return result.scalars().all()



# id 기반 단일 조회 (수정/삭제 전 확인용)
async def read_recommended_challenge_by_id(
    db: AsyncSession, challenge_id: UUID
) -> Optional[RecommendedChallenge]:
    result = await db.execute(
        select(RecommendedChallenge).where(RecommendedChallenge.id == challenge_id)
    )
    return result.scalars().first()



# 수정
async def update_recommended_challenge(
    db: AsyncSession,
    challenge_id: UUID,
    challenge_data: RecommendedChallengeUpdate,
) -> RecommendedChallenge:
    challenge = await read_recommended_challenge_by_id(db, challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="추천 도전 과제를 찾을 수 없습니다.")

    update_data = challenge_data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(challenge, key, value)

    await db.commit()
    await db.refresh(challenge)
    return challenge



# 삭제
async def delete_recommended_challenge(
    db: AsyncSession,
    challenge_id: UUID,
) -> bool:
    challenge = await read_recommended_challenge_by_id(db, challenge_id)
    if not challenge:
        raise HTTPException(status_code=404, detail="삭제할 추천 도전 과제가 없습니다.")

    await db.delete(challenge)
    await db.commit()
    return True