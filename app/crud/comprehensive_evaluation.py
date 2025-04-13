from sqlalchemy.ext.asyncio import AsyncSession
from app.models.evaluation import ComprehensiveEvaluation
from uuid import UUID
from typing import List
from sqlalchemy import select, delete
from app.schemas.comprehensive_evaluation import (
    ComprehensiveEvaluationCreate,
    ComprehensiveEvaluationResponse,
    ComprehensiveEvaluationUpdate,
)
from app.utils.to_snake_case import camel_to_snake


async def create_comprehensive_evaluation(
    db: AsyncSession,
    user_id: UUID,
    comprehensive_evaluation: ComprehensiveEvaluationCreate,
) -> ComprehensiveEvaluationResponse:

    db_comprehensive_evaluation = ComprehensiveEvaluation(
        user_id=user_id,
        overall_achievement_rate=comprehensive_evaluation.overallAchievementRate,
        evaluation_text=comprehensive_evaluation.evaluationText,
        strength_achievement_rate=comprehensive_evaluation.strengthAchievementRate,
        strength_text=comprehensive_evaluation.strengthText,
        improvement_achievement_rate=comprehensive_evaluation.improvementAchievementRate,
    )

    db.add(db_comprehensive_evaluation)
    await db.commit()
    await db.refresh(db_comprehensive_evaluation)
    return db_comprehensive_evaluation


async def read_comprehensive_evaluations(
    db: AsyncSession, user_id: UUID
) -> List[ComprehensiveEvaluationResponse]:
    comprehensive_evaluations = await db.execute(
        select(ComprehensiveEvaluation).where(
            ComprehensiveEvaluation.user_id == user_id
        )
    )
    return comprehensive_evaluations.scalars().all()


async def read_comprehensive_evaluation(
    db: AsyncSession, user_id: UUID, comprehensive_evaluation_id: UUID
) -> ComprehensiveEvaluationResponse:
    comprehensive_evaluation = await db.execute(
        select(ComprehensiveEvaluation).where(
            ComprehensiveEvaluation.id == comprehensive_evaluation_id,
            ComprehensiveEvaluation.user_id == user_id,
        )
    )

    return comprehensive_evaluation.scalars().first()


async def update_comprehensive_evaluation(
    db: AsyncSession,
    user_id: UUID,
    comprehensive_evaluation_id: UUID,
    comprehensive_evaluation: ComprehensiveEvaluationUpdate,
) -> ComprehensiveEvaluationResponse:
    db_comprehensive_evaluation = await read_comprehensive_evaluation(
        db, user_id, comprehensive_evaluation_id
    )

    update_data = comprehensive_evaluation.model_dump(exclude_unset=True)

    # 변환된 키-값 쌍으로 ORM 객체 업데이트
    for key, value in update_data.items():
        snake_key = camel_to_snake(key)

        setattr(db_comprehensive_evaluation, snake_key, value)

    await db.commit()
    await db.refresh(db_comprehensive_evaluation)
    return db_comprehensive_evaluation


async def delete_comprehensive_evaluation(
    db: AsyncSession, user_id: UUID, comprehensive_evaluation_id: UUID
) -> bool:

    delete_statement = delete(ComprehensiveEvaluation).where(
        ComprehensiveEvaluation.id == comprehensive_evaluation_id,
        ComprehensiveEvaluation.user_id == user_id,
    )
    await db.execute(delete_statement)
    await db.commit()
    return True
