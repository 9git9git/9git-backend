from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from enum import Enum as PyEnum
from .base import Base
from category import Goals, TodayNotes, CategoryProgress


# 성별 나누기
class Gender(PyEnum):
    MALE = "M"
    FEMALE = "F"


# User 테이블
class User(Base):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[Gender] = mapped_column(
        Enum(Gender, name="gender_enum"), nullable=False
    )
    age: Mapped[int] = mapped_column(Integer)
    job: Mapped[str] = mapped_column(String(100), nullable=False)

    # User → UserCharacter (1:N 관계)
    user_characters: Mapped[list["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="user"
    )

    # User → Goals (1:N 관계)
    goals: Mapped[list["Goals"]] = relationship("Goals", back_populates="user")

    # User → TodayNotes (1:N 관계)
    today_notes: Mapped[list["TodayNotes"]] = relationship(
        "TodayNotes", back_populates="user"
    )

    # User → CategoryProgress (1:N 관계)
    category_progress: Mapped[list["CategoryProgress"]] = relationship(
        "CategoryProgress", back_populates="user"
    )


# UserCharacter 테이블
class UserCharacter(Base):
    __tablename__ = "user_character"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    character_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("character.id"), nullable=False
    )

    # UserCharacter → User (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="user_characters", cascade="all, delete"
    )

    # UserCharacter → Character (N:1 관계)
    character: Mapped["Character"] = relationship(
        "Character", back_populates="user_characters", cascade="all, delete"
    )


# Character 테이블
class Character(Base):
    __tablename__ = "character"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    image_link: Mapped[str] = mapped_column(String(255), nullable=False)

    # Character → UserCharacter (1:N 관계)
    user_characters: Mapped[list["UserCharacter"]] = relationship(
        "UserCharacter", back_populates="character"
    )
