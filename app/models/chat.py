from sqlalchemy import String, Text, Integer, Enum, ForeignKey, DateTime, CHAR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from uuid import UUID, uuid4
from datetime import datetime, timezone
from .base import Base
from .user import User


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
    category_name: Mapped[str] = mapped_column(
        Enum("파이썬", "영어", "운동", name="category_enum"), nullable=False
    )
    role: Mapped[str] = mapped_column(
        Enum("question", "answer", name="role_enum"), nullable=False
    )
    chat_content: Mapped[str] = mapped_column(Text, nullable=False)

    # 관계 설정: Chats → User, Storages, Functions (N:1 관계)
    user: Mapped["User"] = relationship("User", back_populates="chats")
    storage: Mapped["Storages"] = relationship("Storages", back_populates="chats")
    function: Mapped["Functions"] = relationship("Functions", back_populates="chats")


# Storages 테이블 (저장된 콘텐츠)
class Storages(Base):
    __tablename__ = "storages"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("user.id"), nullable=False
    )
    category_name: Mapped[str] = mapped_column(
        Enum("파이썬", "영어", "운동", name="category_enum"), nullable=False
    )
    function_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("functions.id"), nullable=False
    )
    storage_title: Mapped[str] = mapped_column(String(255), nullable=False)
    storage_description: Mapped[str] = mapped_column(Text, nullable=True)

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
