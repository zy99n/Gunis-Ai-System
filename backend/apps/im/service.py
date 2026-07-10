from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import Conversation, ConversationMember, Message

class ConversationService(BaseService[Conversation]):
    
    async def get_user_conversations(self, db: AsyncSession, user_id: int) -> List[Conversation]:
        """获取用户参与的所有会话"""
        result = await db.execute(
            select(Conversation).join(ConversationMember).where(
                ConversationMember.user_id == user_id
            ).order_by(Conversation.last_message_at.desc())
        )
        return list(result.scalars().all())

class MessageService(BaseService[Message]):
    
    async def get_conversation_messages(self, db: AsyncSession, conversation_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
        """获取会话消息"""
        result = await db.execute(
            select(Message).where(
                Message.conversation_id == conversation_id,
                Message.is_deleted == False
            ).order_by(Message.created_at.asc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

conversation_service = ConversationService(Conversation)
message_service = MessageService(Message)