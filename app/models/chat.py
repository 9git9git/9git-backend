from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base
from .user import User
from enum import Enum as PyEnum
from category import CategoryEnum


# Role Enum 클래스 정의
class RoleEnum(PyEnum):
    QUESTION = "question"
    ANSWER = "answer"


# Chats 테이블 (채팅 기록)
class Chats(Base):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    storage_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("storages.id"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("functions.id"), nullable=False
    )
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    role: Mapped[str] = mapped_column(Enum(RoleEnum, name="role_enum"), nullable=False)
    chat_content: Mapped[str] = mapped_column(Text, nullable=False)

    # 관계 설정: Chats → User, Storages, Functions (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="chats", cascade="all, delete"
    )
    storage: Mapped["Storages"] = relationship(
        "Storages", back_populates="chats", cascade="all, delete"
    )

    function: Mapped["Functions"] = relationship(
        "Functions", back_populates="chats", cascade="all, delete"
    )


# Storages 테이블 (저장된 콘텐츠)
class Storages(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[CategoryEnum] = mapped_column(
        Enum(CategoryEnum, name="category_enum"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("functions.id"), nullable=False
    )
    storage_title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_description: Mapped[str] = mapped_column(Text, nullable=True)

    # 관계 설정: Storages → User, Functions (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="storages", cascade="all, delete"
    )
    function: Mapped["Functions"] = relationship(
        "Functions", back_populates="storages", cascade="all, delete"
    )

    # 관계 설정: Storages → Chats (1:N 관계)
    chats: Mapped[list["Chats"]] = relationship("Chats", back_populates="storage")


# Functions 테이블 (함수 API 정보)
class Functions(Base):
    __tablename__ = "functions"

    function_name: Mapped[str] = mapped_column(String(255), nullable=False)
    function_description: Mapped[str] = mapped_column(Text, nullable=True)
    function_api: Mapped[str] = mapped_column(String(255), nullable=False)

    # 관계 설정: Functions → Storages, Chats (1:N 관계)
    storages: Mapped[list["Storages"]] = relationship(
        "Storages", back_populates="function"
    )
    chats: Mapped[list["Chats"]] = relationship("Chats", back_populates="function")
