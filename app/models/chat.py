from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List
from .base import Base
from .user import User
from .category import Category


# Chat 테이블 (채팅 기록)
class Chat(Base):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    storage_id: Mapped[UUID] = mapped_column(ForeignKey("storages.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    role: Mapped[str] = mapped_column(
        String(20), nullable=False
    )  # 예: 'User', 'Assistant'
    content: Mapped[str] = mapped_column(Text, nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="chats")
    storage: Mapped["Storage"] = relationship("Storage", back_populates="chats")
    category: Mapped["Category"] = relationship("Category")


# Storage 테이블 (저장된 콘텐츠)
class Storage(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship("User", back_populates="storages")
    category: Mapped["Category"] = relationship("Category", back_populates="storages")

    chats: Mapped[List["Chat"]] = relationship(
        "Chat", back_populates="storage", cascade="all, delete"
    )
