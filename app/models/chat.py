from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from .base import Base
from .user import User
from enum import Enum as PyEnum
from .category import CategoryNameEnum


# Role Enum 클래스 정의
class RoleEnum(PyEnum):
    QUESTION = "question"
    ANSWER = "answer"


# Chat 테이블 (채팅 기록)
class Chat(Base):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    storage_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("storages.id"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("functions.id"), nullable=False
    )
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enumss"), nullable=False
    )
    role: Mapped[str] = mapped_column(Enum(RoleEnum, name="role_enums"), nullable=False)
    chat_content: Mapped[str] = mapped_column(Text, nullable=False)

    # Chat → User, Storage, Function (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="chats", cascade="all, delete"
    )
    storage: Mapped["Storage"] = relationship(
        "Storage", back_populates="chats", cascade="all, delete"
    )
    function: Mapped["Function"] = relationship(
        "Function", back_populates="chats", cascade="all, delete"
    )


# Storage 테이블 (저장된 콘텐츠)
class Storage(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("functions.id"), nullable=False
    )
    storage_title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_description: Mapped[str] = mapped_column(Text)

    # Storage → User, Function (N:1 관계)
    user: Mapped["User"] = relationship(
        "User", back_populates="storages", cascade="all, delete"
    )
    function: Mapped["Function"] = relationship(
        "Function", back_populates="storages", cascade="all, delete"
    )

    # Storage → Chat (1:N 관계)
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="storages")


# Function 테이블 (함수 API 정보)
class Function(Base):
    __tablename__ = "functions"

    function_name: Mapped[str] = mapped_column(String(255), nullable=False)
    function_description: Mapped[str] = mapped_column(Text)
    function_api: Mapped[str] = mapped_column(String(255), nullable=False)

    # Function → Storage, Chat (1:N 관계)
    storages: Mapped[list["Storage"]] = relationship(
        "Storage", back_populates="functions"
    )
    chats: Mapped[list["Chat"]] = relationship("Chat", back_populates="functions")
