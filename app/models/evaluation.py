from sqlalchemy import String, Text, Integer, DECIMAL, ForeignKey, DateTime, CHAR, Date
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import uuid4
from datetime import datetime, timezone
from .base import Base
from .user import User
from .category import CategoryProgress


# RecommendedChallenge 테이블 (추천 챌린지)
class RecommendedChallenge(Base):
    __tablename__ = "recommended_challenge"

    user_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("user.user_id"), nullable=False
    )  # User를 참조
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    challenge_task: Mapped[str] = mapped_column(Text, nullable=True)
    challenge_duration: Mapped[str] = mapped_column(String(50), nullable=True)
    challenge_difficulty: Mapped[str] = mapped_column(String(20), nullable=True)
    challenge_suggestion: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정: RecommendedChallenge → User (N:1 관계) / User가 삭제되면 전부삭제
    user: Mapped["User"] = relationship(
        "User", back_populates="recommended_challenges", cascade="all, delete"
    )


# ComprehensiveEvaluations 테이블 (종합 평가)
class ComprehensiveEvaluations(Base):
    __tablename__ = "comprehensive_evaluations"

    evaluation_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("user.user_id"), nullable=False
    )  # User를 참조
    overall_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), nullable=False
    )
    evaluation_text: Mapped[str] = mapped_column(Text, nullable=True)
    strength_category: Mapped[str] = mapped_column(
        String(100), ForeignKey("category_progress.category_name"), nullable=True
    )
    strength_achievement_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    strength_text: Mapped[str] = mapped_column(Text, nullable=True)
    improvement_category: Mapped[str] = mapped_column(
        String(100), ForeignKey("category_progress.category_name"), nullable=False
    )
    monthly_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("monthly_achievements.monthly_id"), nullable=True
    )
    improvement_achievement_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))
    improvement_text: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정: ComprehensiveEvaluations → User (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="comprehensive_evaluations", cascade="all, delete"
    )
    # 관계 설정: ComprehensiveEvaluations → CategoryProgress (N:1 관계)
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="comprehensive_evaluations"
    )
    # 관계 설정: ComprehensiveEvaluations → MonthlyAchievements (N:1 관계)
    monthly_achievement: Mapped["MonthlyAchievements"] = relationship(
        "MonthlyAchievements", back_populates="comprehensive_evaluations"
    )


# MonthlyAchievements 테이블 (월간 성취)
class MonthlyAchievements(Base):
    __tablename__ = "monthly_achievements"

    monthly_id: Mapped[str] = mapped_column(
        CHAR(36), primary_key=True, default=lambda: str(uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("user.user_id"), nullable=False
    )  # User를 참조
    category_name: Mapped[str] = mapped_column(
        String(100), ForeignKey("category_progress.category_name"), nullable=False
    )  # CategoryProgress를 참조
    month_year: Mapped[Date] = mapped_column(Date, nullable=False)
    total_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    completed_goal: Mapped[int] = mapped_column(Integer, nullable=False)
    progress_rate: Mapped[DECIMAL] = mapped_column(DECIMAL(5, 2))

    # 관계 설정: MonthlyAchievements → User, CategoryProgress (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="monthly_achievements")
    category_progress: Mapped["CategoryProgress"] = relationship(
        "CategoryProgress", back_populates="monthly_achievements", cascade="all, delete"
    )
    # 관계 설정: MonthlyAchievements → ComprehensiveEvaluations (1:N 관계)
    comprehensive_evaluations: Mapped[list["ComprehensiveEvaluations"]] = relationship(
        "ComprehensiveEvaluations", back_populates="monthly_achievement"
    )
