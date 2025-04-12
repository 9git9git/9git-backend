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

    # 관계: Week 1 : N Todo (하나의 요일에 여러 할 일이 연결될 수 있음)
    todos: Mapped[Optional[List["app.models.category.Todo"]]] = relationship(
        "app.models.category.Todo", back_populates="week"
    )
