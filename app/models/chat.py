from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, foreign
from uuid import UUID
from typing import List
from .base import Base
from .user import User
from .category import CategoryNameEnum
from app.enum.chat import RoleEnum


# Chat 테이블 (채팅 기록)
class Chat(Base):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    storage_id: Mapped[UUID] = mapped_column(ForeignKey("storages.id"), nullable=False)
    function_id: Mapped[UUID] = mapped_column(
        ForeignKey("functions.id"), nullable=False
    )
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    role: Mapped[str] = mapped_column(Enum(RoleEnum, name="role_enums"), nullable=False)
    chat_content: Mapped[str] = mapped_column(Text, nullable=False)

    # Chat → User, Storage, Function (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="chats")

    # 단일 FK 지정 → foreign_keys 필요 없음
    storage: Mapped["Storage"] = relationship("Storage", back_populates="chats")

    function: Mapped["Function"] = relationship("Function", back_populates="chats")


# Storage 테이블 (저장된 콘텐츠)
class Storage(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_name: Mapped[CategoryNameEnum] = mapped_column(
        Enum(CategoryNameEnum, name="category_name_enums"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        ForeignKey("functions.id"), nullable=False
    )
    storage_title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_description: Mapped[str] = mapped_column(Text)

    # Storage → User, Function (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="storages")
    function: Mapped["Function"] = relationship("Function", back_populates="storages")

    # Storage → Chat (1:N 관계)
    chats: Mapped[List["Chat"]] = relationship(
        "Chat",
        back_populates="storage",
        cascade="all, delete",
        foreign_keys="Chat.storage_id",
    )


# Function 테이블 (함수 API 정보)
class Function(Base):
    __tablename__ = "functions"

    function_name: Mapped[str] = mapped_column(String(255), nullable=False)
    function_description: Mapped[str] = mapped_column(Text)
    function_api: Mapped[str] = mapped_column(String(255), nullable=False)

    # Function → Storage, Chat (1:N 관계)
    storages: Mapped[List["Storage"]] = relationship(
        "Storage", back_populates="function"
    )
    chats: Mapped[List["Chat"]] = relationship("Chat", back_populates="function")
