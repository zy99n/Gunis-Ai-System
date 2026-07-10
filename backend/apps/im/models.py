from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from core.base_model import BaseModel

class Conversation(BaseModel):
    """会话模型"""
    __tablename__ = "conversations"
    
    type = Column(String(20), nullable=False, comment="会话类型: single, group")
    name = Column(String(100), nullable=True, comment="会话名称")
    avatar = Column(String(255), nullable=True, comment="会话头像")
    creator_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="创建人ID")
    last_message_at = Column(DateTime, nullable=True, comment="最后消息时间")
    
    def __repr__(self):
        return f"<Conversation(name={self.name}, id={self.id})>"

class ConversationMember(BaseModel):
    """会话成员模型"""
    __tablename__ = "conversation_members"
    
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, comment="会话ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    last_read_message_id = Column(Integer, nullable=True, comment="最后已读消息ID")
    unread_count = Column(Integer, default=0, comment="未读消息数")
    
    def __repr__(self):
        return f"<ConversationMember(conversation_id={self.conversation_id}, user_id={self.user_id})>"

class Message(BaseModel):
    """消息模型"""
    __tablename__ = "messages"
    
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False, comment="会话ID")
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="发送人ID")
    content = Column(Text, nullable=False, comment="消息内容")
    message_type = Column(String(20), default="text", comment="消息类型: text, image, file, emoji")
    is_read = Column(Boolean, default=False, comment="是否已读")
    
    def __repr__(self):
        return f"<Message(id={self.id}, conversation_id={self.conversation_id})>"