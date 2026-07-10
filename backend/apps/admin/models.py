from sqlalchemy import Column, Integer, String, Text, Boolean
from core.base_model import BaseModel

class SensitiveWord(BaseModel):
    """敏感词模型"""
    __tablename__ = "sensitive_words"
    
    word = Column(String(100), nullable=False, unique=True, comment="敏感词")
    category = Column(String(50), nullable=True, comment="分类")
    replacement = Column(String(50), default="*", comment="替换字符")
    is_active = Column(Boolean, default=True, comment="是否启用")
    
    def __repr__(self):
        return f"<SensitiveWord(word={self.word}, id={self.id})>"

class AuditLog(BaseModel):
    """审计日志模型"""
    __tablename__ = "audit_logs"
    
    user_id = Column(Integer, nullable=True, comment="用户ID")
    username = Column(String(50), nullable=True, comment="用户名")
    action = Column(String(100), nullable=False, comment="操作")
    module = Column(String(50), nullable=True, comment="模块")
    resource_type = Column(String(50), nullable=True, comment="资源类型")
    resource_id = Column(Integer, nullable=True, comment="资源ID")
    description = Column(Text, nullable=True, comment="描述")
    request_ip = Column(String(50), nullable=True, comment="请求IP")
    user_agent = Column(Text, nullable=True, comment="用户代理")
    status = Column(String(20), nullable=True, comment="状态: success, fail")
    error_message = Column(Text, nullable=True, comment="错误信息")
    execution_time_ms = Column(Integer, nullable=True, comment="执行耗时")
    
    def __repr__(self):
        return f"<AuditLog(action={self.action}, id={self.id})>"