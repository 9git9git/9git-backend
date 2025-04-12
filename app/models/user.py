from sqlalchemy import String, Integer, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List, Optional
from .base import Base
from app.enum.user import GenderEnum


# ✅ User 테이블: 사용자 계정 및 기본 프로필 정보
class User(Base):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    password: Mapped[str] = mapped_column(String(255), nullable=False)
    sex: Mapped[Optional[GenderEnum]] = mapped_column(
        SqlEnum(GenderEnum, name="gender_enum")
    )
    age: Mapped[Optional[int]] = mapped_column(Integer)
    job: Mapped[Optional[str]] = mapped_column(String(100))
    level: Mapped[Optional[int]] = mapped_column(Integer, default=1)
    exp: Mapped[Optional[int]] = mapped_column(Integer, default=0)
    character_count: Mapped[Optional[int]] = mapped_column(Integer, default=0)

    # 관계: User 1 : N 다양한 서브 테이블과 연결
    user_characters: Mapped[Optional[List["app.models.user.UserCharacter"]]] = (
        relationship(
            "app.models.user.UserCharacter",
            back_populates="user",
            cascade="all, delete",
        )
    )
    todos: Mapped[Optional[List["app.models.category.Todo"]]] = relationship(
        "app.models.category.Todo",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.category.Todo.user_id",
    )
    memos: Mapped[Optional[List["app.models.category.Memo"]]] = relationship(
        "app.models.category.Memo",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.category.Memo.user_id",
    )
    progresses: Mapped[Optional[List["app.models.category.Progress"]]] = relationship(
        "app.models.category.Progress",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.category.Progress.user_id",
    )
    chats: Mapped[Optional[List["app.models.chat.Chat"]]] = relationship(
        "app.models.chat.Chat",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.chat.Chat.user_id",
    )
    storages: Mapped[Optional[List["app.models.chat.Storage"]]] = relationship(
        "app.models.chat.Storage",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.chat.Storage.user_id",
    )
    comprehensive_evaluations: Mapped[
        Optional[List["app.models.evaluation.ComprehensiveEvaluation"]]
    ] = relationship(
        "app.models.evaluation.ComprehensiveEvaluation",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.evaluation.ComprehensiveEvaluation.user_id",
    )
    recommended_challenges: Mapped[
        Optional[List["app.models.evaluation.RecommendedChallenge"]]
    ] = relationship(
        "app.models.evaluation.RecommendedChallenge",
        back_populates="user",
        cascade="all, delete",
        foreign_keys="app.models.evaluation.RecommendedChallenge.user_id",
    )


# ✅ UserCharacter 테이블: 사용자-캐릭터 연결 다대다 중간 테이블
class UserCharacter(Base):
    __tablename__ = "user_characters"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    character_id: Mapped[UUID] = mapped_column(
        ForeignKey("characters.id"), nullable=False
    )

    # 관계: UserCharacter N : 1 User / Character
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User",
        back_populates="user_characters",
        foreign_keys="UserCharacter.user_id",
    )
    character: Mapped["app.models.user.Character"] = relationship(
        "app.models.user.Character",
        back_populates="user_characters",
        foreign_keys="UserCharacter.character_id",
    )


# ✅ Character 테이블: 유저가 선택 가능한 캐릭터 정보
class Character(Base):
    __tablename__ = "characters"

    character_name: Mapped[str] = mapped_column(String(100), nullable=False)
    level: Mapped[int] = mapped_column(Integer, nullable=False)
    image_link: Mapped[str] = mapped_column(String(255), nullable=False)

    # 관계: Character 1 : N UserCharacter (사용자가 보유한 캐릭터 목록)
    user_characters: Mapped[Optional[List["app.models.user.UserCharacter"]]] = (
        relationship(
            "app.models.user.UserCharacter",
            back_populates="character",
            cascade="all, delete",
        )
    )
