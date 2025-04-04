from sqlalchemy import String, Text, Integer, DECIMAL, ForeignKey, Date, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base
from .user import User
from enum import Enum as PyEnum
from category import CategoryProgresses, CategoryEnum


# RecommendedChallenge 테이블 (추천 챌린지)
class RecommendedChallenges(Base):
    __tablename__ = "recommended_challenges"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )  # User를 참조
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), defalt=0.00)
    challenge_task: Mapped[str] = mapped_column(Text, nullable=True)
    challenge_duration: Mapped[str] = mapped_column(String(50), nullable=True)
    challenge_difficulty: Mapped[str] = mapped_column(String(20), nullable=True)
    challenge_suggestion: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정: RecommendedChallenge → User (N:1 관계) / User가 삭제되면 전부 삭제
    user: Mapped["User"] = relationship(
        "User", back_populates="recommended_challenges", cascade="all, delete"
    )

    # 관계 설정: RecommendedChallenge → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgresses"] = relationship(
        "CategoryProgresses",
        back_populates="recommended_challenges",
        cascade="all, delete",
    )


# ComprehensiveEvaluations 테이블 (종합 평가)
class ComprehensiveEvaluations(Base):
    __tablename__ = "comprehensive_evaluations"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )  # User를 참조
    overall_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00
    )
    evaluation_text: Mapped[str] = mapped_column(Text, nullable=True)
    strength_category: Mapped[str] = mapped_column(String(100), nullable=False)
    strength_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00
    )
    strength_text: Mapped[str] = mapped_column(Text, nullable=True)
    improvement_category: Mapped[str] = mapped_column(String(100), nullable=False)
    improvement_achievement_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    improvement_text: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정: ComprehensiveEvaluations → User (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="comprehensive_evaluations", cascade="all, delete"
    )

    # 관계 설정: ComprehensiveEvaluations → MonthlyAchievements (N:1 관계)
    monthly_achievements: Mapped["MonthlyAchievements"] = relationship(
        "MonthlyAchievements",
        back_populates="comprehensive_evaluations",
        cascade="all, delete",
    )

    # 관계 설정: ComprehensiveEvaluations → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgresses"] = relationship(
        "CategoryProgresses",
        back_populates="comprehensive_evaluations",
        cascade="all, delete",
    )


# MonthlyAchievements 테이블 (월간 성취)
class MonthlyAchievements(Base):
    __tablename__ = "monthly_achievements"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )  # User를 참조
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    month_year: Mapped[Date] = mapped_column(Date, nullable=False)
    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2), default=0.00)

    # 관계 설정: MonthlyAchievements → User
    user: Mapped["User"] = relationship("User", back_populates="monthly_achievements")

    # 관계 설정 : MonthlyAchievements -> ConprehensiveEvaluations (1 : N 관계)
    comprehensive_evaluations: Mapped[list["ComprehensiveEvaluations"]] = relationship(
        "ComprehensiveEvaluations", back_populates="monthly_achievements"
    )
