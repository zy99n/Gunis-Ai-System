from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import conversation_service, message_service
from .schemas import MessageCreate, MessageResponse, ConversationResponse, CreateConversationRequest
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/conversations", response_model=List[ConversationResponse])
async def get_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await conversation_service.get_user_conversations(db, current_user.id)

@router.get("/conversations/{id}", response_model=ConversationResponse)
async def get_conversation(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = await conversation_service.get_by_id(db, id)
    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")
    return conversation

@router.post("/conversations/private")
async def create_private_conversation(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = await conversation_service.create(db, {
        "type": "single",
        "creator_id": current_user.id
    })
    await db.execute(
        conversation_service.model.__table__.insert().values(
            conversation_id=conversation.id,
            user_id=current_user.id
        )
    )
    await db.execute(
        conversation_service.model.__table__.insert().values(
            conversation_id=conversation.id,
            user_id=user_id
        )
    )
    await db.commit()
    return {"message": "创建成功", "conversation_id": conversation.id}

@router.post("/conversations/group")
async def create_group_conversation(
    name: str,
    user_ids: List[int],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = await conversation_service.create(db, {
        "type": "group",
        "name": name,
        "creator_id": current_user.id
    })
    await db.commit()
    return {"message": "创建成功", "conversation_id": conversation.id}

@router.get("/conversations/{id}/messages", response_model=List[MessageResponse])
async def get_messages(
    id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await message_service.get_conversation_messages(db, id, skip=skip, limit=limit)

@router.post("/conversations/{id}/messages", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def send_message(
    id: int,
    data: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conversation = await conversation_service.get_by_id(db, id)
    if not conversation:
        raise HTTPException(status_code=404, detail="会话不存在")
    
    return await message_service.create(db, {
        "conversation_id": id,
        "sender_id": current_user.id,
        "content": data.content,
        "message_type": data.message_type
    })