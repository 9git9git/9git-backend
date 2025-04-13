from app.schemas.base import ResponseBase
from app.schemas.comprehensive_evaluation import (
    ComprehensiveEvaluationResponse,
    ComprehensiveEvaluationCreate,
    ComprehensiveEvaluationUpdate,
)
from app.services.comprehensive_evaluation import (
    select_comprehensive_evaluation,
    select_comprehensive_evaluations,
    add_comprehensive_evaluation,
    update_comprehensive_evaluation_service,
    delete_comprehensive_evaluation_service,
)
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import get_db
from uuid import UUID
from typing import List
from fastapi import HTTPException
from fastapi import status

router = APIRouter()


@router.get(
    "/",
    response_model=ResponseBase[List[ComprehensiveEvaluationResponse]],
)
async def get_comprehensive_evaluations(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[ComprehensiveEvaluationResponse]]:

    try:
        comprehensive_evaluations = await select_comprehensive_evaluations(db, user_id)
        return ResponseBase(
            status_code=status.HTTP_200_OK, data=comprehensive_evaluations
        )
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get(
    "/{comprehensive_evaluation_id}",
    response_model=ResponseBase[ComprehensiveEvaluationResponse],
)
async def get_comprehensive_evaluation(
    user_id: UUID,
    comprehensive_evaluation_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResponse]:
    try:
        comprehensive_evaluation = await select_comprehensive_evaluation(
            db, user_id, comprehensive_evaluation_id
        )
        return ResponseBase(
            status_code=status.HTTP_200_OK, data=comprehensive_evaluation
        )
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post(
    "/",
    response_model=ResponseBase[ComprehensiveEvaluationResponse],
)
async def post_comprehensive_evaluation(
    comprehensive_evaluation: ComprehensiveEvaluationCreate,
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResponse]:
    try:
        comprehensive_evaluation = await add_comprehensive_evaluation(
            db, user_id, comprehensive_evaluation
        )
        return ResponseBase(
            status_code=status.HTTP_201_CREATED, data=comprehensive_evaluation
        )
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put(
    "/{comprehensive_evaluation_id}",
    response_model=ResponseBase[ComprehensiveEvaluationResponse],
)
async def put_comprehensive_evaluation(
    user_id: UUID,
    comprehensive_evaluation_id: UUID,
    comprehensive_evaluation: ComprehensiveEvaluationUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ComprehensiveEvaluationResponse]:
    try:
        comprehensive_evaluation = await update_comprehensive_evaluation_service(
            db, user_id, comprehensive_evaluation_id, comprehensive_evaluation
        )
        return ResponseBase(
            status_code=status.HTTP_200_OK, data=comprehensive_evaluation
        )
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{comprehensive_evaluation_id}", response_model=ResponseBase[bool])
async def delete_comprehensive_evaluation(
    user_id: UUID,
    comprehensive_evaluation_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_comprehensive_evaluation_service(
            db, user_id, comprehensive_evaluation_id
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
