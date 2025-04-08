from sqlalchemy import (
    String,
    Text,
    Integer,
    DECIMAL,
    ForeignKey,
    Date,
    Enum,
    ForeignKeyConstraint,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from enum import Enum as PyEnum
from .base import Base
from .user import User
from .category import CategoryProgress, CategoryNameEnum


class StrengthCategoryEnum(PyEnum):
    CODING = "코딩"
    ENGLISH = "영어"
    EXERCISE = "운동"


class ImprovementCategoryEnum(PyEnum):
    CODING = "코딩"
    ENGLISH = "영어"
    EXERCISE = "운동"


# RecommendedChallenge 테이블 (추천 챌린지)
class RecommendedChallenge(Base):
    __tablename__ = "recommended_challenges"

    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("category_progresses.id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )  # CategoryProgresses클래스의 user_id 참조
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    progress_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    challenge_task: Mapped[str] = mapped_column(Text)
    challenge_duration: Mapped[str] = mapped_column(String(50))
    challenge_difficulty: Mapped[str] = mapped_column(String(20))
    challenge_suggestion: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        ForeignKeyConstraint(
            ["progress_id", "user_id", "category_name"],
            [
                "category_progresses.id",
                "category_progresses.user_id",
                "category_progresses.category_name",
            ],
        ),
    )

    # RecommendedChallenge → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="recommended_challenges"
    )


# ComprehensiveEvaluation 테이블 (종합 평가)
class ComprehensiveEvaluation(Base):
    __tablename__ = "comprehensive_evaluations"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("category_progresses.id"), nullable=False
    )
    overall_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    evaluation_text: Mapped[str] = mapped_column(Text)
    strength_category: Mapped[StrengthCategoryEnum] = mapped_column(
        Enum(StrengthCategoryEnum, name="strength_category_enums"), nullable=False
    )
    strength_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    strength_text: Mapped[str] = mapped_column(Text)
    improvement_category: Mapped[ImprovementCategoryEnum] = mapped_column(
        Enum(ImprovementCategoryEnum, name="improvement_category_enums"), nullable=False
    )
    improvement_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    improvement_text: Mapped[str] = mapped_column(Text)

    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "progress_id"],
            ["category_progresses.user_id", "category_progresses.id"],
        ),
    )

    # ComprehensiveEvaluation → User, MonthlyAchievement, CategoryProgress (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="comprehensive_evaluations"
    )
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="comprehensive_evaluations"
    )


# MonthlyAchievement 테이블 (월간 성취)
class MonthlyAchievement(Base):
    __tablename__ = "monthly_achievements"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    month_year: Mapped[Date] = mapped_column(Date, nullable=False)
    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    __table_args__ = (
        ForeignKeyConstraint(
            ["user_id", "category_name"],
            ["category_progresses.user_id", "category_progresses.category_name"],
        ),
    )
    # MonthlyAchievement → User, CategoryProgress (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="monthly_achievements")
    category_progress: Mapped[List["CategoryProgress"]] = relationship(
        "CategoryProgress", back_populates="monthly_achievements"
    )
