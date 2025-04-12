# category.py (ERD 기반 주석 및 관계 FK 명시)
from sqlalchemy import (
    String,
    Boolean,
    Integer,
    Text,
    Date,
    DECIMAL,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from .base import Base
from .user import User
from .week import Week
from app.enum.category import CategoryNameEnum, CategoryColorEnum


# Category 테이블 (카테고리 이름 및 색상)
class Category(Base):
    __tablename__ = "categories"

    category_name: Mapped[CategoryNameEnum] = mapped_column(nullable=False)
    category_color: Mapped[CategoryColorEnum] = mapped_column(nullable=False)

    # 관계: Progress, Todo, Memo, Storage와 연결됨 1 : N
    progresses: Mapped[List["Progress"]] = relationship(
        "Progress", back_populates="category", cascade="all, delete"
    )
    todos: Mapped[List["Todo"]] = relationship(
        "Todo", back_populates="category", cascade="all, delete"
    )
    memos: Mapped[List["Memo"]] = relationship(
        "Memo", back_populates="category", cascade="all, delete"
    )
    storages: Mapped[List["Storage"]] = relationship(
        "Storage", back_populates="category", cascade="all, delete"
    )


# Progress 테이블 (카테고리 별 진행률)
class Progress(Base):
    __tablename__ = "progresses"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), default=0.00)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # 관계
    user: Mapped["User"] = relationship(
        "User", back_populates="progresses", foreign_keys="Progress.user_id"
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="progresses", foreign_keys="Progress.category_id"
    )
    # todos, memos 랑 연결이 필요한가?================================================
    todos: Mapped[List["Todo"]] = relationship(
        "Todo", back_populates="progress", cascade="all, delete"
    )
    memos: Mapped[List["Memo"]] = relationship(
        "Memo", back_populates="progress", cascade="all, delete"
    )
    # =============================================================================
    comprehensive_evaluations: Mapped[
        List["app.models.evaluation.ComprehensiveEvaluation"]
    ] = relationship(
        "app.models.evaluation.ComprehensiveEvaluation",
        back_populates="progress",
        cascade="all, delete",
    )
    recommended_challenges: Mapped[
        List["app.models.evaluation.RecommendedChallenge"]
    ] = relationship(
        "app.models.evaluation.RecommendedChallenge",
        back_populates="progress",
        cascade="all, delete",
    )


# Todo 테이블 (할 일 관리)
class Todo(Base):
    __tablename__ = "todos"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    # Todo인데 progress_id가 필요할까?
    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("progresses.id"), nullable=False
    )
    week_id: Mapped[UUID] = mapped_column(ForeignKey("weeks.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_repeat: Mapped[bool] = mapped_column(Boolean, default=False)

    # 관계
    user: Mapped["User"] = relationship(
        "User", back_populates="todos", foreign_keys="Todo.user_id"
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="todos", foreign_keys="Todo.category_id"
    )
    # 필요 한가?
    progress: Mapped["Progress"] = relationship(
        "Progress", back_populates="todos", foreign_keys="Todo.progress_id"
    )
    week: Mapped["Week"] = relationship(
        "Week", back_populates="todos", foreign_keys="Todo.week_id"
    )


# Memo 테이블 (메모/노트)
class Memo(Base):
    __tablename__ = "memos"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    # 필요 한가?
    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("progresses.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # 관계 N : 1
    user: Mapped["User"] = relationship(
        "User", back_populates="memos", foreign_keys="Memo.user_id"
    )
    category: Mapped["Category"] = relationship(
        "Category", back_populates="memos", foreign_keys="Memo.category_id"
    )
    # 필요 한가?
    progress: Mapped["Progress"] = relationship(
        "Progress", back_populates="memos", foreign_keys="Memo.progress_id"
    )
