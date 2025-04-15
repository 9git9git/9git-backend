from app.models.week import Week
from sqlalchemy import select, delete, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.models.category import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from sqlalchemy.orm import selectinload
from app.utils.to_snake_case import camel_to_snake
from datetime import date, timedelta
from app.enum.week import WeekdayEnum


# 할 일 생성
async def create_todo(
    db: AsyncSession, user_id: UUID, category_id: UUID, todo_data: TodoCreate
) -> TodoResponse:
    todo = Todo(
        user_id=user_id,
        category_id=category_id,
        content=todo_data.content,
        start_date=todo_data.startDate,
        end_date=todo_data.endDate,
        is_completed=todo_data.isCompleted,
        is_repeat=todo_data.isRepeat,
    )
    # 우선 Todo 먼저 생성
    # 먼저 이렇게 처리르 안해주면 아래 관계 데이터 생성 때 Todo.id가 없어서 오류 발생 commit 전까지는 데이터가 없음
    db.add(todo)
    await db.commit()
    await db.refresh(todo)

    # Todo 생성 후 관계 데이터인 Week 생성
    if todo_data.weeks:
        for week in todo_data.weeks:
            week = Week(
                week_name=week.weekName,
                todo_id=todo.id,
            )
            db.add(week)

    db.add(todo)
    await db.commit()
    await db.refresh(todo)

    return TodoResponse(
        id=todo.id,
        user_id=todo.user_id,
        category_id=todo.category_id,
        content=todo.content,
        start_date=todo.start_date,
        end_date=todo.end_date,
        is_completed=todo.is_completed,
        is_repeat=todo.is_repeat,
        # 관계 데이터인 Week는 따로 조회로직이 필요한데 create todo response에서는 굳이 넣지 않음
        weeks=None,
    )


# 특정 유저의 전체 할 일 목록 조회
async def read_all_todos(db: AsyncSession, user_id: UUID) -> List[TodoResponse]:
    result = await db.execute(
        select(Todo)
        .options(selectinload(Todo.weeks), selectinload(Todo.category))
        .where(Todo.user_id == user_id)
    )
    return result.scalars().all()


# 특정 유저의 특정 할 일 조회 (응답용)
async def read_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> Optional[TodoResponse]:
    result = await db.execute(
        select(Todo)
        .options(selectinload(Todo.weeks), selectinload(Todo.category))
        .where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    return result.scalars().first()


# 특정 유저의 특정 할 일 조회 (내부 처리용)
async def read_raw_todo_by_id(
    db: AsyncSession, user_id: UUID, todo_id: UUID
) -> Optional[Todo]:
    result = await db.execute(
        select(Todo).where(Todo.id == todo_id, Todo.user_id == user_id)
    )
    return result.scalars().first()


# 특정 유저의 특정 카테고리에 속한 할 일 목록 조회
async def read_todos_by_user_and_category(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> List[TodoResponse]:
    result = await db.execute(
        select(Todo)
        .options(selectinload(Todo.weeks), selectinload(Todo.category))
        .where(Todo.user_id == user_id, Todo.category_id == category_id)
    )
    return result.scalars().all()


# 수정
async def update_todo(
    db: AsyncSession, todo: Todo, todo_data: TodoUpdate
) -> TodoResponse:
    # 1. Todo 기본 필드 업데이트 (weeks 제외)
    update_data = todo_data.model_dump(exclude_unset=True, exclude={"weeks"})

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(todo, snake_key, value)

    # 2. weeks 관련 업데이트 처리
    if todo_data.weeks is not None:
        # 기존 weeks 삭제
        await db.execute(delete(Week).where(Week.todo_id == todo.id))

        # 새 weeks 추가
        for week in todo_data.weeks:
            week_name = week.weekName if hasattr(week, "weekName") else week.week_name
            new_week = Week(week_name=week_name, todo_id=todo.id)
            db.add(new_week)

    # 변경사항 저장
    await db.commit()
    await db.refresh(todo)

    # TodoResponse 객체 반환
    return TodoResponse(
        id=todo.id,
        user_id=todo.user_id,
        category_id=todo.category_id,
        content=todo.content,
        start_date=todo.start_date,
        end_date=todo.end_date,
        is_completed=todo.is_completed,
        is_repeat=todo.is_repeat,
        weeks=None,
    )


# 삭제
async def delete_todo(db: AsyncSession, todo: Todo) -> bool:
    delete_stmt = delete(Todo).where(Todo.id == todo.id)
    try:
        await db.execute(delete_stmt)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True


# 날짜 범위로 할 일 조회 (반복 요일 고려)
async def read_todos_by_date_range(
    db: AsyncSession, user_id: UUID, start_date: date, end_date: date
) -> List[TodoResponse]:
    """
    주어진 날짜 범위 내에 있는 Todo를 조회합니다.

    1. 일반 Todo: 날짜 범위와 겹치는 모든 Todo를 반환
    2. 반복 Todo: 날짜 범위 내에서 지정된 요일에 반복되는 Todo를 반환
    """
    # 기본 쿼리: 해당 기간과 겹치는 모든 Todo 가져오기
    query = (
        select(Todo)
        .options(
            selectinload(Todo.weeks),
            selectinload(Todo.category),
        )
        .where(
            and_(
                Todo.user_id == user_id,
                or_(
                    # Case 1: Todo 시작일이 검색 기간 내에 있음
                    and_(Todo.start_date >= start_date, Todo.start_date <= end_date),
                    # Case 2: Todo 종료일이 검색 기간 내에 있음
                    and_(Todo.end_date >= start_date, Todo.end_date <= end_date),
                    # Case 3: Todo 기간이 검색 기간을 포함
                    and_(Todo.start_date <= start_date, Todo.end_date >= end_date),
                ),
            )
        )
    )

    result = await db.execute(query)
    todos = list(result.scalars().all())
    todo_responses = []

    # 각 Todo에 대해 처리
    for todo in todos:
        if not todo.is_repeat or not todo.weeks:
            # 반복이 아닌 Todo는 그대로 추가
            todo_responses.append(todo)
        else:
            # 반복 Todo의 경우 해당 날짜 범위의 각 날짜를 확인
            # 각 요일별로 해당 Todo를 반환
            # Todo 객체의 내용을 복사하되, 시작/종료 날짜를 해당 날짜로 설정
            weekday_map = {
                WeekdayEnum.MONDAY: 0,
                WeekdayEnum.TUESDAY: 1,
                WeekdayEnum.WEDNESDAY: 2,
                WeekdayEnum.THURSDAY: 3,
                WeekdayEnum.FRIDAY: 4,
                WeekdayEnum.SATURDAY: 5,
                WeekdayEnum.SUNDAY: 6,
            }

            # Todo에 설정된 반복 요일들
            todo_weekdays = {weekday_map[week.week_name] for week in todo.weeks}

            # 해당 기간의 모든 날짜를 순회
            current_date = max(start_date, todo.start_date)
            end = min(end_date, todo.end_date)

            while current_date <= end:
                # 해당 날짜의 요일이 Todo의 반복 요일에 포함되는지 확인
                if current_date.weekday() in todo_weekdays:
                    todo_responses.append(todo)
                    break  # 이미 추가했으므로 나머지는 건너뜀

                current_date += timedelta(days=1)

    return todo_responses
