from sqlalchemy import String, Boolean, Integer, Text, Date, DECIMAL, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base
from .evaluation import ComprehensiveEvaluations
from .user import User
from enum import Enum as PyEnum
from evaluation import RecommendedChallenges


# 카테고리 Enum 클래스 정의
class CategoryEnum(PyEnum):
    CODING = "코딩"
    ENGLISH = "영어"
    WORKOUT = "운동"


# 색상 Enum 클래스 정의
class CategoryColor(PyEnum):
    CODING = "#FDA63A"  # 호박색
    ENGLISH = "#6C88C4"  # 인디고 블루
    WORKOUT = "#556B2F"  # 올리브 그린


# CategoryProgress 테이블 (한 카테고리에 여러 목표, 노트가 연결됨)
class CategoryProgresses(Base):
    __tablename__ = "category_progresses"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )

    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), default=0.00)

    user: Mapped["User"] = relationship(
        "User", back_populates="category_progress", cascade="all, delete"
    )

    # CategoryProgresses -> Goals (N : 1 관계)
    goals: Mapped[list["Goals"]] = relationship(
        "Goals", back_populates="category_progress", cascade="all, delete"
    )

    # CategoryProgesses -> ComprehensiveEvaluations (1 : N 관계)
    comprehensive_evaluations: Mapped[list["ComprehensiveEvaluations"]] = relationship(
        "ComprehensiveEvaluations", back_populates="category_progress"
    )

    # CategoryProgesses -> RecommandedChallenges (1 : N 관계)
    recommended_challenges: Mapped[list["RecommendedChallenges"]] = relationship(
        "RecommendedChallenges", back_populates="category_progress"
    )


# 목표 관리 테이블 (Goals) (여러 목표가 한 카테고리에 연결됨)
class Goals(Base):
    __tablename__ = "goals"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    category_color: Mapped[CategoryColor] = mapped_column(
        Enum(CategoryColor, name="category_color_enum"), nullable=False
    )
    todo_content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_repeat: Mapped[bool] = mapped_column(Boolean, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="goals", cascade="all, delete"
    )

    # Goals -> CategoryProgresses (1 : N 관계)
    category_progress: Mapped["CategoryProgresses"] = relationship(
        "CategoryProgresses", back_populates="goals"
    )


# 오늘의 노트 테이블 (TodayNotes) (여러 노트가 한 카테고리에 연결됨)
class TodayNotes(Base):
    __tablename__ = "today_notes"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship(
        "User", back_populates="today_notes", cascade="all, delete"
    )
