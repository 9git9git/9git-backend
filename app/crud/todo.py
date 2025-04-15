from app.models.week import Week
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import List, Optional
from app.models.category import Todo
from app.schemas.todo import TodoCreate, TodoUpdate, TodoResponse
from sqlalchemy.orm import selectinload
from app.utils.to_snake_case import camel_to_snake


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
