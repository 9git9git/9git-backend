from decimal import Decimal
from app.crud.progress import read_progress_by_user_and_category
from app.models.week import Week
from sqlalchemy import select, delete, and_
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.models.category import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from sqlalchemy.orm import selectinload
from app.utils.to_snake_case import camel_to_snake
from datetime import date


# 할 일 생성
async def create_todo(
    db: AsyncSession, user_id: UUID, category_id: UUID, todo_data: TodoCreate
) -> TodoResponse:
    try:
        # Todo 생성
        todo = Todo(
            user_id=user_id,
            category_id=category_id,
            content=todo_data.content,
            start_date=todo_data.startDate,
            end_date=todo_data.endDate,
            is_completed=todo_data.isCompleted,
            is_repeat=todo_data.isRepeat,
        )
        db.add(todo)
        await db.flush()  # ID 할당을 위해 flush

        # Todo 생성 후 관계 데이터인 Week 생성 (빈 배열이 아닌 경우만)
        if todo_data.weeks is not None and len(todo_data.weeks) > 0:
            for week in todo_data.weeks:
                week_obj = Week(
                    week_name=week.weekName,
                    todo_id=todo.id,
                )
                db.add(week_obj)

        await db.flush()

        # 카테고리 진행률 업데이트
        await update_category_progress(db, user_id, category_id)

        # 모든 작업 완료 후 명시적으로 커밋
        await db.commit()

        # 최신 상태로 객체 새로고침
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
            weeks=None,
        )
    except Exception as e:
        # 에러 발생 시 롤백 처리
        await db.rollback()
        raise e


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


# 날짜 범위로 할 일 조회 (기본)
async def read_todos_by_period(
    db: AsyncSession, user_id: UUID, start_date: date, end_date: date
) -> List[Todo]:

    # 해당 기간과 겹치는 모든 Todo 가져오기 (간소화된 조건)
    query = (
        select(Todo)
        .options(selectinload(Todo.weeks), selectinload(Todo.category))
        .where(
            Todo.user_id == user_id,
            # 모든 겹침 케이스를 처리하는 단일 조건
            Todo.start_date <= end_date,
            Todo.end_date >= start_date,
        )
    )

    result = await db.execute(query)

    # unique -> 조인 쿼리 시 중복 데이터 제거
    return result.unique().scalars().all()


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


# 진행률 업데이트 함수
async def update_category_progress(
    db: AsyncSession, user_id: UUID, category_id: UUID
) -> None:
    # 카테고리에 속한 모든 할 일 조회
    todos = await read_todos_by_user_and_category(db, user_id, category_id)

    # 전체 Todo 개수와 완료된 Todo 개수 계산
    total_todos = len(todos)
    completed_todos = sum(1 for todo in todos if todo.is_completed)

    # 진행률 계산 (완료된 할 일 / 전체 할 일 * 100)
    progress_rate = Decimal(0)
    if total_todos > 0:
        progress_rate = Decimal(completed_todos / total_todos * 100)

    # 해당 카테고리의 Progress 조회
    progress = await read_progress_by_user_and_category(db, user_id, category_id)

    if progress:
        progress.progress_rate = progress_rate
        # 변경된 객체를 세션에 등록
        db.add(progress)


# 수정
async def update_todo(
    db: AsyncSession, todo: Todo, todo_data: TodoUpdate
) -> TodoResponse:
    try:
        original_category_id = todo.category_id

        # 1. Todo 기본 필드 업데이트 (weeks 제외)
        update_data = todo_data.model_dump(exclude_unset=True, exclude={"weeks"})
        for key, value in update_data.items():
            snake_key = camel_to_snake(key)
            setattr(todo, snake_key, value)

        # 2. weeks 관련 업데이트 처리
        if (
            todo_data.weeks is not None
        ):  # weeks가 명시적으로 제공된 경우 (None이 아닌 경우)
            # 기존 weeks 삭제
            await db.execute(delete(Week).where(Week.todo_id == todo.id))

            # 새 weeks 추가 (빈 배열이 아닌 경우만)
            if len(todo_data.weeks) > 0:
                for week in todo_data.weeks:
                    week_name = (
                        week.weekName if hasattr(week, "weekName") else week.week_name
                    )
                    new_week = Week(week_name=week_name, todo_id=todo.id)
                    db.add(new_week)

        await db.flush()  # 업데이트 작업을 flush

        # 3. 진행률 업데이트 호출
        await update_category_progress(db, todo.user_id, todo.category_id)
        # 카테고리가 변경된 경우 이전 카테고리 진행률도 업데이트
        if (
            "categoryId" in update_data
            and update_data["categoryId"] != original_category_id
        ):
            await update_category_progress(db, todo.user_id, original_category_id)

        # 4. 모든 작업 완료 후 명시적으로 커밋
        await db.commit()

        # 5. 최신 상태로 객체 새로고침
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
            weeks=None,
        )
    except Exception as e:
        # 에러 발생 시 롤백 처리
        await db.rollback()
        raise e


# 삭제
async def delete_todo(db: AsyncSession, todo: Todo) -> bool:
    try:
        user_id = todo.user_id
        category_id = todo.category_id

        # Todo 삭제
        delete_stmt = delete(Todo).where(Todo.id == todo.id)
        await db.execute(delete_stmt)

        await db.flush()  # 업데이트 작업을 flush
        # 진행률 업데이트
        await update_category_progress(db, user_id, category_id)

        await db.commit()

        return True

    except Exception as e:
        # 예외 발생 시 트랜잭션은 자동 롤백됨
        await db.rollback()
        raise e
