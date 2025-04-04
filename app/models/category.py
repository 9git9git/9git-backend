from sqlalchemy import (
    String,
    Boolean,
    Integer,
    Text,
    Date,
    DECIMAL,
    ForeignKey,
    DateTime,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from .base import Base
from .evaluation import ComprehensiveEvaluations


# CategoryProgress 테이블 (한 카테고리에 여러 목표, 노트가 연결됨)
class CategoryProgress(Base):
    __tablename__ = "category_progress"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(
        String(100), primary_key=True
    )  # ✅ 카테고리 이름을 기본 키로 설정
    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), nullable=True)

    # 관계 설정: CategoryProgress → Goals, TodayNotes (1:N 관계)
    goals: Mapped[list["Goals"]] = relationship(
        "Goals", back_populates="category_progress", cascade="all, delete"
    )
    today_notes: Mapped[list["TodayNotes"]] = relationship(
        "TodayNotes", back_populates="category_progress", cascade="all, delete-orphan"
    )
    comprehensive_evaluations: Mapped[list["ComprehensiveEvaluations"]] = relationship(
        "ComprehensiveEvaluations", back_populates="category_progress"
    )


# 목표 관리 테이블 (Goals) (여러 목표가 한 카테고리에 연결됨)
class Goals(Base):
    __tablename__ = "goals"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("category_progress.category_name"), nullable=False
    )  # ✅ 카테고리 참조 추가
    todo_content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_repeat: Mapped[bool] = mapped_column(Boolean, nullable=False)

    # Goals → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="goals", cascade="all, delete"
    )


# 오늘의 노트 테이블 (TodayNotes) (여러 노트가 한 카테고리에 연결됨)
class TodayNotes(Base):
    __tablename__ = "today_notes"

    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("category_progress.category_name"), nullable=False
    )  # ✅ 카테고리 참조 추가
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # TodayNotes → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="today_notes", cascade="all, delete"
    )
