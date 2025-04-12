from sqlalchemy import (
    String,
    Text,
    DECIMAL,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import Optional
from .base import Base


# ✅ RecommendedChallenge 테이블: 진행률 기반으로 추천되는 개인화 챌린지
class RecommendedChallenge(Base):
    __tablename__ = "recommended_challenges"

    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    progress_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    challenge_task: Mapped[str] = mapped_column(Text)
    challenge_duration: Mapped[str] = mapped_column(String(50))
    challenge_difficulty: Mapped[str] = mapped_column(String(20))
    challenge_suggestion: Mapped[str] = mapped_column(Text)

    # 관계: RecommendedChallenge N : 1 User / Category
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="recommended_challenges"
    )
    category: Mapped[Optional["app.models.category.Category"]] = relationship(
        "app.models.category.Category",
        back_populates="recommended_challenges",
        foreign_keys="RecommendedChallenge.category_id",
    )


# ✅ ComprehensiveEvaluation 테이블: 사용자의 전체 평가 및 피드백 저장
class ComprehensiveEvaluation(Base):
    __tablename__ = "comprehensive_evaluations"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    overall_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    evaluation_text: Mapped[str] = mapped_column(Text)
    strength_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    strength_text: Mapped[str] = mapped_column(Text)
    improvement_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    improvement_text: Mapped[str] = mapped_column(Text)

    # 관계: ComprehensiveEvaluation N : 1 User
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="comprehensive_evaluations"
    )
