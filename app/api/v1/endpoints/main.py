from http.client import HTTPException
from app.schemas.main import TodosAndMemosResponse
from app.services.main import select_todos_and_memos_by_period
from app.schemas.base import ResponseBase
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date
from app.db.session import get_db
from app.schemas.progress import TodayProgressResponse
from app.services.main import select_today_progresses

router = APIRouter()


@router.get("/todos-and-memos", response_model=ResponseBase[TodosAndMemosResponse])
async def get_todos_and_memos(
    user_id: UUID,
    start_date: date,
    end_date: date,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodosAndMemosResponse]:
    try:
        todos_and_memos = await select_todos_and_memos_by_period(
            db, user_id, start_date, end_date
        )
        return ResponseBase(status_code=status.HTTP_200_OK, data=todos_and_memos)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/today-progresses", response_model=ResponseBase[TodayProgressResponse])
async def get_today_progresses(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[TodayProgressResponse]:
    try:
        today_progresses = await select_today_progresses(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=today_progresses)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
