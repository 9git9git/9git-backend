from app.enum.week import WeekdayEnum
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List
from datetime import date, timedelta

from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from app.crud.todo import (
    create_todo,
    read_all_todos,
    read_todo_by_id,
    read_raw_todo_by_id,
    update_todo,
    delete_todo,
    read_todos_by_user_and_category,
    read_todos_by_period,
)


# ✅ 할 일 생성
async def add_todo(
    db: AsyncSession, user_id: UUID, category_id: UUID, todo_data: TodoCreate
) -> TodoResponse:
    try:
        return await create_todo(db, user_id, category_id, todo_data)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e


# ✅ 특정 유저의 전체 할 일 목록 조회
async def select_all_todos(db: AsyncSession, user_id: UUID) -> List[TodoResponse]:
    return await read_all_todos(db, user_id)


# ✅ 특정 유저의 특정 할 일 조회
async def select_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> TodoResponse:
    todo = await read_todo_by_id(db, user_id, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )
    return todo


# ✅ 유저 + 카테고리별 Todo 목록 조회
async def select_todos_by_user_and_category(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[TodoResponse]:
    return await read_todos_by_user_and_category(db, user_id, category_id)


# ✅ 날짜 범위로 할 일 조회 (반복 요일 고려)
async def select_todos_by_period(
    db: AsyncSession, user_id: UUID, start_date: date, end_date: date
) -> List[TodoResponse]:
    try:

        # 1. 기본 Todo 데이터 조회
        todos = await read_todos_by_period(db, user_id, start_date, end_date)

        # 2. 검색 기간 내 각 날짜의 요일 계산
        period_weekdays = set()
        current = start_date
        while current <= end_date:
            weekday_num = current.weekday()  # 0=월, 1=화, ... 6=일
            # WeekdayEnum 형식으로 변환
            weekday_names = {
                0: WeekdayEnum.MONDAY,
                1: WeekdayEnum.TUESDAY,
                2: WeekdayEnum.WEDNESDAY,
                3: WeekdayEnum.THURSDAY,
                4: WeekdayEnum.FRIDAY,
                5: WeekdayEnum.SATURDAY,
                6: WeekdayEnum.SUNDAY,
            }
            period_weekdays.add(weekday_names[weekday_num])
            current += timedelta(days=1)

        # 3. 결과 필터링 - 반복 일정인 경우 요일 확인
        filtered_todos = []
        for todo in todos:
            # 3.1 반복이 아닌 일정은 그대로 포함
            if not todo.is_repeat or not hasattr(todo, "weeks") or not todo.weeks:
                filtered_todos.append(todo)
                continue

            # 3.2 반복 일정인 경우, 검색 기간의 요일과 Todo의 요일 확인
            todo_weekdays = {week.week_name for week in todo.weeks}

            # 검색 기간의 요일과 Todo의 요일이 하나라도 일치하면 포함
            if todo_weekdays.intersection(period_weekdays):
                filtered_todos.append(todo)

        return filtered_todos

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"할 일 조회 중 오류가 발생했습니다: {str(e)}",
        ) from e


# ✅ 할 일 수정
async def update_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID, todo_data: TodoUpdate
) -> TodoResponse:
    todo = await read_raw_todo_by_id(db, user_id, todo_id)
    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Todo를 찾을 수 없습니다.",
        )
    return await update_todo(db, todo, todo_data)


# ✅ 할 일 삭제
async def delete_todo_service(db: AsyncSession, user_id: UUID, todo_id: UUID) -> bool:
    try:
        todo = await read_raw_todo_by_id(db, user_id, todo_id)
        if not todo:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Todo를 찾을 수 없습니다.",
            )
        return await delete_todo(db, todo)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        ) from e
