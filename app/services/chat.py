from typing import List
from uuid import UUID
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.chat import (
    ChatCreate,
    ChatUpdate,
    ChatResponse,
)
from app.crud.chat import (
    read_chat,
    read_chats_by_user,
    read_chats_by_storage,
    read_chats_by_category,
    create_chat,
    update_chat,
    delete_chat,
)


# 단일 조회
async def select_chat(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
) -> ChatResponse:
    return await read_chat(db, user_id, chat_id)


# 전체 조회
async def select_chats_by_user(
    db: AsyncSession,
    user_id: UUID,
) -> List[ChatResponse]:
    return await read_chats_by_user(db, user_id)


# storage_id 기준 조회
async def select_chats_by_storage(
    db: AsyncSession,
    user_id: UUID,
    storage_id: UUID,
) -> List[ChatResponse]:
    return await read_chats_by_storage(db, user_id, storage_id)


# category_id 기준 조회
async def select_chats_by_category(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
) -> List[ChatResponse]:
    return await read_chats_by_category(db, user_id, category_id)


# 생성
async def add_chat(
    db: AsyncSession,
    user_id: UUID,
    storage_id: UUID,
    category_id: UUID,
    chat_data: ChatCreate,
) -> ChatResponse:
    return await create_chat(db, user_id, storage_id, category_id, chat_data)


# 수정
async def update_chat_service(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
    chat_data: ChatUpdate,
) -> ChatResponse:
    db_chat = await read_chat(db, user_id, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="채팅 정보를 찾을 수 없습니다.",
        )
    return await update_chat(db, user_id, chat_id, chat_data)


# 삭제
async def delete_chat_service(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
) -> bool:
    db_chat = await read_chat(db, user_id, chat_id)
    if not db_chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="채팅 정보를 찾을 수 없습니다.",
        )
    return await delete_chat(db, user_id, chat_id)
