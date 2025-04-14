from uuid import UUID
from typing import List
from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat import Chat
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse
from app.utils.to_snake_case import camel_to_snake


# 생성
async def create_chat(
    db: AsyncSession,
    user_id: UUID,
    storage_id: UUID,
    category_id: UUID,
    chat_data: ChatCreate,
) -> ChatResponse:

    new_chat = Chat(
        user_id=user_id,
        storage_id=storage_id,
        category_id=category_id,
        role=chat_data.role,
        content=chat_data.content,
    )

    db.add(new_chat)
    await db.commit()
    await db.refresh(new_chat)
    return new_chat


# 단일 채팅 조회
async def read_chat(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
) -> ChatResponse:
    result = await db.execute(
        select(Chat).where(Chat.id == chat_id, Chat.user_id == user_id)
    )
    return result.scalars().first()


# 전체 채팅 조회 (user_id 기준)
async def read_chats_by_user(
    db: AsyncSession,
    user_id: UUID,
) -> List[ChatResponse]:
    result = await db.execute(select(Chat).where(Chat.user_id == user_id))
    return result.scalars().all()


# 특정 storage에 속한 채팅 조회
async def read_chats_by_storage(
    db: AsyncSession,
    user_id: UUID,
    storage_id: UUID,
) -> List[ChatResponse]:
    result = await db.execute(
        select(Chat).where(Chat.user_id == user_id, Chat.storage_id == storage_id)
    )
    return result.scalars().all()


# 특정 category에 속한 채팅 조회
async def read_chats_by_category(
    db: AsyncSession,
    user_id: UUID,
    category_id: UUID,
) -> List[ChatResponse]:
    result = await db.execute(
        select(Chat).where(Chat.user_id == user_id, Chat.category_id == category_id)
    )
    return result.scalars().all()


# 수정
async def update_chat(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
    chat_data: ChatUpdate,
) -> ChatResponse:
    db_chat = await read_chat(db, user_id, chat_id)

    update_data = chat_data.model_dump(exclude_unset=True)

    # 변환된 키-값 쌍으로 ORM 객체 업데이트
    for key, value in update_data.items():
        snake_key = camel_to_snake(key)

        setattr(db_chat, snake_key, value)

    await db.commit()
    await db.refresh(db_chat)
    return db_chat


# 삭제
async def delete_chat(
    db: AsyncSession,
    user_id: UUID,
    chat_id: UUID,
) -> bool:
    delete_statement = delete(Chat).where(
        Chat.id == chat_id,
        Chat.user_id == user_id,
    )
    try:
        await db.execute(delete_statement)
        await db.commit()
    except Exception as e:
        await db.rollback()
        raise e
    return True
