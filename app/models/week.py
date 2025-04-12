from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from .base import Base
from app.enum.week import WeekdayEnum


# Week 테이블 (요일 정의용)
class Week(Base):
    __tablename__ = "weeks"

    week_name: Mapped[WeekdayEnum] = mapped_column(
        Enum(WeekdayEnum, name="week_name_enums"), nullable=False
    )

    # 관계 1:N
    todos: Mapped[List["app.models.category.Todo"]] = relationship(
        "app.models.category.Todo",
        back_populates="week",
        cascade="all, delete",
        foreign_keys="app.models.category.Todo.week_id",
    )
