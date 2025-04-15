from app.schemas.main import TodosAndMemosResponse
from app.schemas.progress import TodayProgressResponse
from app.services.progress import select_all_progresses
from app.services.todo import select_todos_by_period
from app.services.memo import select_memos_by_period
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import date


async def select_todos_and_memos_by_period(
    db: AsyncSession, user_id: UUID, start_date: date, end_date: date
) -> TodosAndMemosResponse:
    todos = await select_todos_by_period(db, user_id, start_date, end_date)
    memos = await select_memos_by_period(db, user_id, start_date, end_date)
    return TodosAndMemosResponse(todos=todos, memos=memos)


async def select_today_progresses(
    db: AsyncSession, user_id: UUID
) -> TodayProgressResponse:
    today = date.today()

    # 2. 오늘의 모든 Todo 가져오기
    today_todos = await select_todos_by_period(db, user_id, today, today)

    # 3. 전체 Todo 개수와 완료된 Todo 개수 계산
    total_todos = len(today_todos)
    completed_todos = sum(1 for todo in today_todos if todo.is_completed)

    # 4. 전체 달성률 계산 (Todo가 없으면 0%)
    total_progress_rate = 0
    if total_todos > 0:
        total_progress_rate = (completed_todos / total_todos) * 100

    # 5. 카테고리별 진행률 가져오기
    category_progresses = await select_all_progresses(db, user_id)
    return TodayProgressResponse(
        totalProgressRate=total_progress_rate,
        cheerUpMessage="오늘도 화이팅!",
        categoryProgresses=category_progresses,
    )
