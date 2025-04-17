from uuid import UUID
from typing import List
from sqlalchemy import select, delete, text
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.chat import Chat
from app.models.category import Category
from app.schemas.chat import (
    ChatCreate,
    ChatUpdate,
    ChatResponse,
    ModelResponse,
    ChatWithModelResponse,
)
from app.enum.chat import RoleEnum
from app.utils.to_snake_case import camel_to_snake
from app.utils.chat_model_selector import route_to_model
from app.enum.category import CategoryNameEnum
from app.models.category import Category


# 생성
async def create_chat(
    db: AsyncSession,
    user_id: UUID,
    storage_id: UUID,
    category_id: UUID,
    chat_data: ChatCreate,
) -> ChatWithModelResponse:

    user_chat = Chat(
        user_id=user_id,
        storage_id=storage_id,
        category_id=category_id,
        role=chat_data.role,
        content=chat_data.content,
    )
    db.add(user_chat)
    await db.commit()
    await db.refresh(user_chat)

    # ✅ 카테고리 이름 직접 SQL로 조회 (ENUM)
    result = await db.execute(
        text(
            """
        SELECT category_name
        FROM categories
        WHERE id = :category_id
        """
        ),
        {"category_id": str(category_id)},
    )
    row = result.first()

    if row is None:
        raise ValueError("❌ 해당 category_id에 대한 카테고리를 찾을 수 없습니다.")

    category_enum = CategoryNameEnum[row.category_name]

    # ✅ GPT 호출
    if chat_data.role == RoleEnum.USER:
        model_func = route_to_model(category_enum)
        gpt_response = model_func(chat_data.content)

        assistant_chat = Chat(
            user_id=user_id,
            storage_id=storage_id,
            category_id=category_id,
            role=RoleEnum.ASSISTANT,
            content=gpt_response,
        )
        db.add(assistant_chat)
        await db.commit()
        await db.refresh(assistant_chat)

        return ChatWithModelResponse(
            chat=user_chat, model_response=ModelResponse(content=gpt_response)
        )

    # assistant role이 아닌 경우
    return ChatWithModelResponse(
        chat=user_chat, model_response=ModelResponse(content="")
    )


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
