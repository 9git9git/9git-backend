from typing import List
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.base import ResponseBase
from app.schemas.chat import ChatCreate, ChatUpdate, ChatResponse, ChatWithModelResponse
from app.services.chat import (
    select_chat,
    select_chats_by_user,
    select_chats_by_storage,
    select_chats_by_category,
    add_chat,
    update_chat_service,
    delete_chat_service,
)

router = APIRouter()


@router.get("/", response_model=ResponseBase[List[ChatResponse]])
async def get_chats_by_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[ChatResponse]]:
    try:
        chats = await select_chats_by_user(db, user_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=chats)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/storage/{storage_id}", response_model=ResponseBase[List[ChatResponse]])
async def get_chats_by_storage(
    user_id: UUID,
    storage_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[ChatResponse]]:
    try:
        chats = await select_chats_by_storage(db, user_id, storage_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=chats)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/", response_model=ResponseBase[List[ChatResponse]])
async def get_chats_by_category(
    user_id: UUID,
    category_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[List[ChatResponse]]:
    try:
        chats = await select_chats_by_category(db, user_id, category_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=chats)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.get("/{chat_id}", response_model=ResponseBase[ChatResponse])
async def get_chat(
    user_id: UUID,
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ChatResponse]:
    try:
        chat = await select_chat(db, user_id, chat_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=chat)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.post("/", response_model=ResponseBase[ChatWithModelResponse])
async def post_chat(
    user_id: UUID,
    storage_id: UUID,
    category_id: UUID,
    chat_data: ChatCreate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ChatWithModelResponse]:
    try:
        chat_result = await add_chat(db, user_id, storage_id, category_id, chat_data)
        return ResponseBase(status_code=status.HTTP_201_CREATED, data=chat_result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.put("/{chat_id}", response_model=ResponseBase[ChatResponse])
async def put_chat(
    user_id: UUID,
    chat_id: UUID,
    chat_data: ChatUpdate,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[ChatResponse]:
    try:
        chat = await update_chat_service(db, user_id, chat_id, chat_data)
        return ResponseBase(status_code=status.HTTP_200_OK, data=chat)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )


@router.delete("/{chat_id}", response_model=ResponseBase[bool])
async def delete_chat(
    user_id: UUID,
    chat_id: UUID,
    db: AsyncSession = Depends(get_db),
) -> ResponseBase[bool]:
    try:
        result = await delete_chat_service(db, user_id, chat_id)
        return ResponseBase(status_code=status.HTTP_200_OK, data=result)
    except HTTPException as e:
        return ResponseBase(status_code=e.status_code, error=e.detail)
    except Exception as e:
        return ResponseBase(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, error=str(e)
        )
