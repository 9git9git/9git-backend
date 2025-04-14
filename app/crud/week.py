from app.utils.to_snake_case import camel_to_snake
from sqlalchemy import select, delete
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from app.models.week import Week
from app.schemas.week import WeekCreate, WeekUpdate


async def create_week(db: AsyncSession, todo_id: UUID, week_data: WeekCreate) -> Week:
    db_week = Week(
        todo_id=todo_id,
        week_name=week_data.weekName,
    )
    db.add(db_week)
    await db.commit()
    await db.refresh(db_week)
    return db_week


async def read_weeks(db: AsyncSession, todo_id: UUID) -> List[Week]:
    db_weeks = await db.execute(select(Week).where(Week.todo_id == todo_id))
    return db_weeks.scalars().all()


async def read_week_by_id(db: AsyncSession, todo_id: UUID, week_id: UUID) -> Week:
    db_week = await db.execute(
        select(Week).where(Week.id == week_id, Week.todo_id == todo_id)
    )
    return db_week.scalars().first()


async def update_week(
    db: AsyncSession, todo_id: UUID, week_id: UUID, week_data: WeekUpdate
) -> Week:
    db_week = await read_week_by_id(db, todo_id, week_id)
    update_data = week_data.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        snake_key = camel_to_snake(key)
        setattr(db_week, snake_key, value)

    await db.commit()
    await db.refresh(db_week)
    return db_week


async def delete_week(db: AsyncSession, todo_id: UUID, week_id: UUID) -> bool:
    delete_statement = delete(Week).where(Week.id == week_id, Week.todo_id == todo_id)
    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
