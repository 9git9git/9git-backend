from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from enum import Enum as PyEnum
from .base import Base
from .category import Goal, TodayNote, CategoryProgress
from .chat import Chat, Storage
from .evaluation import ComprehensiveEvaluation, MonthlyAchievement
from typing import List


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
    sex: Mapped[GenderEnum] = mapped_column(Enum(GenderEnum, name="gender_enum"))
    age: Mapped[int] = mapped_column(Integer)
    job: Mapped[str] = mapped_column(String(100))
    level: Mapped[int] = mapped_column(Integer, default=1)
    exp: Mapped[int] = mapped_column(Integer, default=0)
    character_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # User → UserCharacter, Goal, TodayNote, CategoryProgress, Chat, Storage, ComprehensiveEvaluation, MonthlyAchievement (1:N 관계)
    user_characters: Mapped[List["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="user", cascade="all, delete"
    )
    goals: Mapped[List["Goal"]] = relationship(
        "Goal", back_populates="user", cascade="all, delete"
    )
    today_notes: Mapped[List["TodayNote"]] = relationship(
        "TodayNote", back_populates="user", cascade="all, delete"
    )
    category_progresses: Mapped[List["CategoryProgress"]] = relationship(
        "CategoryProgress", back_populates="user", cascade="all, delete"
    )
    chats: Mapped[List["Chat"]] = relationship(
        "Chat", back_populates="user", cascade="all, delete"
    )
    storages: Mapped[List["Storage"]] = relationship(
        "Storage", back_populates="user", cascade="all, delete"
    )
    comprehensive_evaluations: Mapped[List["ComprehensiveEvaluation"]] = relationship(
        "ComprehensiveEvaluation", back_populates="user", cascade="all, delete"
    )
    monthly_achievements: Mapped[List["MonthlyAchievement"]] = relationship(
        "MonthlyAchievement", back_populates="user", cascade="all, delete"
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
    user: Mapped["User"] = relationship("User", back_populates="user_characters")
    character: Mapped["Character"] = relationship(
        "Character", back_populates="user_characters"
    )


# Character 테이블
class Character(Base):
    __tablename__ = "characters"

    character_name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    image_link: Mapped[str] = mapped_column(String(255), nullable=False)

    # Character → UserCharacter (1:N 관계)
    user_characters: Mapped[List["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="characters", cascade="all, delete"
    )
