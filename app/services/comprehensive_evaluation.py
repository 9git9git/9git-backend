from app.schemas.comprehensive_evaluation import (
    ComprehensiveEvaluationCreate,
    ComprehensiveEvaluationResponse,
    ComprehensiveEvaluationUpdate,
)
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
from app.crud.comprehensive_evaluation import (
    read_comprehensive_evaluation,
    read_comprehensive_evaluations,
    create_comprehensive_evaluation,
    update_comprehensive_evaluation,
    delete_comprehensive_evaluation,
)

from uuid import UUID


async def select_comprehensive_evaluation(
    db: AsyncSession, user_id: UUID, comprehensive_evaluation_id: UUID
) -> ComprehensiveEvaluationResponse:
    return await read_comprehensive_evaluation(db, user_id, comprehensive_evaluation_id)


async def select_comprehensive_evaluations(
    db: AsyncSession, user_id: UUID
) -> List[ComprehensiveEvaluationResponse]:
    return await read_comprehensive_evaluations(db, user_id)


async def add_comprehensive_evaluation(
    db: AsyncSession,
    user_id: UUID,
    comprehensive_evaluation: ComprehensiveEvaluationCreate,
) -> ComprehensiveEvaluationResponse:
    return await create_comprehensive_evaluation(db, user_id, comprehensive_evaluation)


async def update_comprehensive_evaluation_service(
    db: AsyncSession,
    user_id: UUID,
    comprehensive_evaluation_id: UUID,
    comprehensive_evaluation: ComprehensiveEvaluationUpdate,
) -> ComprehensiveEvaluationResponse:
    db_comprehensive_evaluation = await read_comprehensive_evaluation(
        db, user_id, comprehensive_evaluation_id
    )

    if not db_comprehensive_evaluation:
        raise HTTPException(status_code=404, detail="종합평가 정보를 찾을 수 없습니다.")

    return await update_comprehensive_evaluation(
        db, user_id, comprehensive_evaluation_id, comprehensive_evaluation
    )


async def delete_comprehensive_evaluation_service(
    db: AsyncSession, user_id: UUID, comprehensive_evaluation_id: UUID
) -> bool:
    db_comprehensive_evaluation = await read_comprehensive_evaluation(
        db, user_id, comprehensive_evaluation_id
    )
    if not db_comprehensive_evaluation:
        raise HTTPException(status_code=404, detail="종합평가 정보를 찾을 수 없습니다.")

    return await delete_comprehensive_evaluation(
        db, user_id, comprehensive_evaluation_id
    )
