from pydantic import BaseModel, Field
from typing import Optional

class MessageCreate(BaseModel):
    content: str = Field(..., description="消息内容")
    message_type: Optional[str] = Field("text", description="消息类型")

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    sender_id: int
    content: str
    message_type: str
    is_read: bool
    created_at: str
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    type: str
    name: Optional[str]
    avatar: Optional[str]
    creator_id: int
    last_message_at: Optional[str]
    unread_count: int = 0
    created_at: str
    
    class Config:
        from_attributes = True

class CreateConversationRequest(BaseModel):
    type: str = Field(..., description="会话类型")
    name: Optional[str] = Field(None, description="会话名称")
    user_ids: Optional[list] = Field(None, description="用户ID列表")