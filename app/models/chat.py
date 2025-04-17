from sqlalchemy import String, Text, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from uuid import UUID
from typing import List, Optional
from .base import Base
from app.enum.chat import RoleEnum


# ✅ Chat 테이블: 챗봇 또는 사용자 간 대화 기록 저장
class Chat(Base):
    __tablename__ = "chats"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    storage_id: Mapped[UUID] = mapped_column(ForeignKey("storages.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    role: Mapped[RoleEnum] = mapped_column(
        SqlEnum(RoleEnum, name="role_enum"), nullable=False
    )
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # 관계: Chat N : 1 User / Storage / Category
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="chats"
    )
    storage: Mapped[Optional["app.models.chat.Storage"]] = relationship(
        "app.models.chat.Storage", back_populates="chats"
    )
    category: Mapped[Optional["app.models.category.Category"]] = relationship(
        "app.models.category.Category", back_populates="chats"
    )


# ✅ Storage 테이블: 저장된 대화/메모/기록을 포함하는 컨테이너 테이블
class Storage(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"), nullable=False)
    category_id: Mapped[UUID] = mapped_column(
        ForeignKey("categories.id"), nullable=False
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    # 관계: Storage N : 1 User / Category
    user: Mapped["app.models.user.User"] = relationship(
        "app.models.user.User", back_populates="storages"
    )
    category: Mapped[Optional["app.models.category.Category"]] = relationship(
        "app.models.category.Category", back_populates="storages"
    )

    # 관계: Storage 1 : N Chat
    chats: Mapped[Optional[List["app.models.chat.Chat"]]] = relationship(
        "app.models.chat.Chat", back_populates="storage", cascade="all, delete"
    )
