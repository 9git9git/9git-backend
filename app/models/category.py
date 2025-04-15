from sqlalchemy import String, Boolean, Text, Date, DECIMAL, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List, Optional
from .base import Base
from app.enum.category import CategoryNameEnum, CategoryColorEnum


# ✅ Category 테이블: 사용자의 카테고리를 정의 (코딩/영어/운동 등)
class Category(Base):
    __tablename__ = "categories"

    category_name: Mapped[CategoryNameEnum] = mapped_column(nullable=False)
    category_color: Mapped[CategoryColorEnum] = mapped_column(nullable=False)

    # 관계: Category 1 : 1 Progress
    progress: Mapped["app.models.category.Progress"] = relationship(
        "app.models.category.Progress",
        back_populates="category",
        cascade="all, delete",
    )

    # 관계: Category 1 : N Todo, Memo, Storage, RecommendedChallenge
    todos: Mapped[Optional[List["app.models.category.Todo"]]] = relationship(
        "app.models.category.Todo", back_populates="category", cascade="all, delete"
    )
    memos: Mapped[Optional[List["app.models.category.Memo"]]] = relationship(
        "app.models.category.Memo", back_populates="category", cascade="all, delete"
    )
    storages: Mapped[Optional[List["app.models.chat.Storage"]]] = relationship(
        "app.models.chat.Storage", back_populates="category", cascade="all, delete"
    )
    recommended_challenges: Mapped[
        Optional[List["app.models.evaluation.RecommendedChallenge"]]
    ] = relationship(
        "app.models.evaluation.RecommendedChallenge",
        back_populates="category",
        cascade="all, delete",
    )


# ✅ Progress 테이블: 카테고리별 목표 진행률 저장 테이블
class Progress(Base):
    __tablename__ = "progresses"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), default=0.00)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # 관계: Progress N : 1 User
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User",
        back_populates="progresses",
        foreign_keys="Progress.user_id",
    )
    # 관계: Progress 1 : 1 Category
    category: Mapped["app.models.category.Category"] = relationship(
        "app.models.category.Category",
        back_populates="progress",
        foreign_keys="Progress.category_id",
    )


# ✅ Todo 테이블: 할 일(Task) 기록 테이블
class Todo(Base):
    __tablename__ = "todos"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    is_repeat: Mapped[bool] = mapped_column(Boolean, default=False)

    # 관계: Todo N : 1 User / Category
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="todos", foreign_keys="Todo.user_id"
    )
    category: Mapped[Optional["app.models.category.Category"]] = relationship(
        "app.models.category.Category",
        back_populates="todos",
        foreign_keys="Todo.category_id",
    )
    # 관계: Todo 1 : N Week
    weeks: Mapped[Optional[List["app.models.week.Week"]]] = relationship(
        "app.models.week.Week",
        back_populates="todo",
        foreign_keys="app.models.week.Week.todo_id",
    )


# ✅ Memo 테이블: 사용자 개인 메모 및 노트 저장 테이블
class Memo(Base):
    __tablename__ = "memos"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    start_date: Mapped[Date] = mapped_column(Date, nullable=False)
    end_date: Mapped[Date] = mapped_column(Date, nullable=False)

    # 관계: Memo N : 1 User / Category
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="memos", foreign_keys="Memo.user_id"
    )
    category: Mapped[Optional["app.models.category.Category"]] = relationship(
        "app.models.category.Category",
        back_populates="memos",
        foreign_keys="Memo.category_id",
    )
