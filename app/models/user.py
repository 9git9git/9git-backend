from sqlalchemy import String, Integer, Enum, ForeignKey, Date, DECIMAL, Boolean, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from enum import Enum as PyEnum
from .base import Base
from .category import Goal, TodayNote, CategoryProgress
from .chat import Chat, Storage
from .evaluation import (
    RecommendedChallenge,
    ComprehensiveEvaluation,
    MonthlyAchievement,
)


# 성별 Enum 클래스
class GenderEnum(PyEnum):
    MALE = "M"
    FEMALE = "F"


# User 테이블
class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[GenderEnum] = mapped_column(
        Enum(GenderEnum, name="gender_enum"), nullable=False
    )
    age: Mapped[int] = mapped_column(Integer)
    job: Mapped[str] = mapped_column(String(100), nullable=False)

    # User → UserCharacter, Goal, TodayNote, CategoryProgress, Chat, Storage, ComprehensiveEvaluation, MonthlyAchievement, RecommendedChallenge (1:N 관계)
    user_characters: Mapped[list["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="users"
    )
    goals: Mapped[list["Goal"]] = relationship("Goal", back_populates="users")
    today_notes: Mapped[list["TodayNote"]] = relationship(
        "TodayNote", back_populates="users"
    )
    category_progresses: Mapped[list["CategoryProgress"]] = relationship(
        "CategoryProgress", back_populates="users"
    )
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="users")
    storages: Mapped[list["Storage"]] = relationship("Storage", back_populates="users")
    comprehensive_evaluations: Mapped[list["ComprehensiveEvaluation"]] = relationship(
        "ComprehensiveEvaluation", back_populates="users"
    )
    monthly_achievements: Mapped[list["MonthlyAchievement"]] = relationship(
        "MonthlyAchievement", back_populates="users"
    )
    recommended_challenges: Mapped[list["RecommendedChallenge"]] = relationship(
        "RecommendedChallenge", back_populates="users"
    )


# UserCharacter 테이블
class UserCharacter(Base):
    __tablename__ = "user_characters"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    character_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("characters.id"), nullable=False
    )

    # UserCharacter → User, Character (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="user_characters", cascade="all, delete"
    )
    character: Mapped["Character"] = relationship(
        "Character", back_populates="user_characters", cascade="all, delete"
    )


# Character 테이블
class Character(Base):
    __tablename__ = "characters"

    character_name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    image_link: Mapped[str] = mapped_column(String(255), nullable=False)

    # Character → UserCharacter (1:N 관계)
    user_characters: Mapped[list["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="characters"
    )
