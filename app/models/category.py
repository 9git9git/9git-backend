from sqlalchemy import (
    String,
    Boolean,
    Integer,
    Text,
    Date,
    DECIMAL,
    ForeignKey,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from enum import Enum as PyEnum
from typing import List
from .base import Base
from .user import User


#  CategoryNameEnum 클래스 정의
class CategoryNameEnum(PyEnum):
    CODING = "코딩"
    ENGLISH = "영어"
    EXERCISE = "운동"


# CategoryColorEnum 클래스 정의
class CategoryColorEnum(PyEnum):
    CODING = "#FDA63A"  # 호박색
    ENGLISH = "#6C88C4"  # 인디고 블루
    EXERCISE = "#556B2F"  # 올리브 그린


# CategoryProgress 테이블 (한 카테고리에 여러 목표, 노트가 연결됨)
class CategoryProgress(Base):
    __tablename__ = "category_progresses"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )

    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), default=0.00)

    # CategoryProgress → User (N : 1 관계)
    user: Mapped["User"] = relationship("User", back_populates="category_progresses")

    # CategoryProgress → ComprehensiveEvaluation, RecommendedChallenge, Goal, MonthlyAchievement (1 : N 관계)
    comprehensive_evaluations: Mapped[
        List["app.models.evaluation.ComprehensiveEvaluation"]
    ] = relationship(
        "app.models.evaluation.ComprehensiveEvaluation",
        back_populates="category_progress",
        cascade="all, delete",
    )
    recommended_challenges: Mapped[
        List["app.models.evaluation.RecommendedChallenge"]
    ] = relationship(
        "app.models.evaluation.RecommendedChallenge",
        back_populates="category_progress",
        cascade="all, delete",
        foreign_keys="[app.models.evaluation.RecommendedChallenge.progress_id]",  # 추가
    )
    goals: Mapped[List["Goal"]] = relationship(
        "Goal", back_populates="category_progress", cascade="all, delete"
    )
    monthly_achievements: Mapped[List["app.models.evaluation.MonthlyAchievement"]] = (
        relationship(
            "app.models.evaluation.MonthlyAchievement",
            back_populates="category_progress",
            cascade="all, delete",
        )
    )


# 목표 관리 테이블 (Goal) (여러 목표가 한 카테고리에 연결됨)
class Goal(Base):
    __tablename__ = "goals"

    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("category_progresses.id"), nullable=False
    )

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    category_color: Mapped[CategoryColorEnum] = mapped_column(
        Enum(CategoryColorEnum, name="category_color_enums"), nullable=False
    )
    todo_content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_repeat: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="goals")
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="goals"
    )


# 오늘의 노트 테이블 (TodayNote) (여러 노트가 한 카테고리에 연결됨)
class TodayNote(Base):
    __tablename__ = "today_notes"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # TodayNote → User (N : 1 관계)
    user: Mapped["User"] = relationship("User", back_populates="today_notes")
