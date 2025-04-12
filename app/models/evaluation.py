from sqlalchemy import (
    String,
    Text,
    Integer,
    DECIMAL,
    ForeignKey,
    Date,
    Enum,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from .base import Base
from .user import User
from .category import Progress


# RecommendedChallenge 테이블 (추천 과제)
class RecommendedChallenge(Base):
    __tablename__ = "recommended_challenges"

    # 외래키: 사용자의 특정 진행 중 카테고리와 연결됨
    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("progresses.id"), nullable=False
    )
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)

    progress_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    challenge_task: Mapped[str] = mapped_column(Text)
    challenge_duration: Mapped[str] = mapped_column(String(50))
    challenge_difficulty: Mapped[str] = mapped_column(String(20))
    challenge_suggestion: Mapped[str] = mapped_column(Text)

    # 관계 설정 N : 1
    user: Mapped["User"] = relationship("User", back_populates="recommended_challenges")
    progress: Mapped["Progress"] = relationship(
        "Progress",
        back_populates="recommended_challenges",
        foreign_keys="RecommendedChallenge.progress_id",
    )


# ComprehensiveEvaluation 테이블 (종합 평가)
class ComprehensiveEvaluation(Base):
    __tablename__ = "comprehensive_evaluations"

    # 외래키 설정
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    progress_id: Mapped[UUID] = mapped_column(
        ForeignKey("progresses.id"), nullable=False
    )

    overall_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    evaluation_text: Mapped[str] = mapped_column(Text)

    # 강점 관련 필드
    strength_category: Mapped[str] = mapped_column(String(50), nullable=False)
    strength_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    strength_text: Mapped[str] = mapped_column(Text)

    # 개선점 관련 필드
    improvement_category: Mapped[str] = mapped_column(String(50), nullable=False)
    improvement_achievement_rate: Mapped[DECIMAL] = mapped_column(
        DECIMAL(5, 2), default=0.00, nullable=False
    )
    improvement_text: Mapped[str] = mapped_column(Text)

    # 관계 설정 N : 1
    user: Mapped["User"] = relationship(
        "User", back_populates="comprehensive_evaluations"
    )
    progress: Mapped["Progress"] = relationship(
        "Progress",
        back_populates="comprehensive_evaluations",
        foreign_keys="ComprehensiveEvaluation.progress_id",
    )
