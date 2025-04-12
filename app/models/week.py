from sqlalchemy import Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from typing import List, Optional
from .base import Base
from app.enum.week import WeekdayEnum


# ✅ Week 테이블: 요일 정보 저장 (월~일)
class Week(Base):
    __tablename__ = "weeks"

    week_name: Mapped[WeekdayEnum] = mapped_column(
        SqlEnum(WeekdayEnum, name="week_name_enums"), nullable=False
    )

    # 관계: Todo N : 1 Week (하나의 할 일이 하나의 요일을 갖고, 여러 Todo가 같은 요일을 가질 수 있음)
    todo: Mapped[Optional["app.models.category.Todo"]] = relationship(
        "app.models.category.Todo", back_populates="weeks"
    )
