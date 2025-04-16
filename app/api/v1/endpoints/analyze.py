from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.schemas.base import ResponseBase
from app.schemas.comprehensive_evaluation import ComprehensiveEvaluationResponse
from app.schemas.recommended_challenge import RecommendedChallengeResponse
from app.services.analyze import (
    get_or_create_today_comprehensive_evaluation,
    get_or_create_today_recommended_challenges,
)
from app.db.session import get_db
from typing import List

router = APIRouter()


@router.get(
    "/today",
    response_model=ResponseBase[ComprehensiveEvaluationResponse],
)
async def get_today_analysis(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResponse]:
    """
    오늘의 종합 평가를 가져오거나 생성합니다.
    """
    try:
        result = await get_or_create_today_comprehensive_evaluation(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get(
    "/today/challenges",
    response_model=ResponseBase[List[RecommendedChallengeResponse]],
)
async def get_today_challenges(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[RecommendedChallengeResponse]]:
    """
    오늘의 추천 도전과제를 가져오거나 생성합니다.
    """
    try:
        result = await get_or_create_today_recommended_challenges(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
