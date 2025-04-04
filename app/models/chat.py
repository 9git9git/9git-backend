from sqlalchemy import String, Text, Integer, Enum, ForeignKey, DateTime, CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import uuid4
from datetime import datetime, timezone
from .base import Base  # ✅ 공통적인 Base 클래스 임포트
from .user import User


# Chats 테이블 (채팅 기록)
class Chats(Base):
    __tablename__ = "chats"

    user_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("user.user_id"), nullable=False
    )
    storage_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("storages.storage_id"), nullable=False
    )
    function_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("functions.function_id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    role: Mapped[str] = mapped_column(
        Enum("question", "answer", name="role_enum"), nullable=False
    )
    chat_content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 관계 설정: Chats → User, Storages, Functions (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="chats")
    storage: Mapped["Storages"] = relationship("Storages", back_populates="chats")
    function: Mapped["Functions"] = relationship("Functions", back_populates="chats")


# Storages 테이블 (저장된 콘텐츠)
class Storages(Base):
    __tablename__ = "storages"

    user_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("user.user_id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(String(100), nullable=False)
    function_id: Mapped[str] = mapped_column(
        CHAR(36), ForeignKey("functions.function_id"), nullable=False
    )
    storage_title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_description: Mapped[str] = mapped_column(Text, nullable=True)
    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # 관계 설정: Storages → User, Functions (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="storages")
    function: Mapped["Functions"] = relationship("Functions", back_populates="storages")

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
