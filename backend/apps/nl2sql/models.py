from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from core.base_model import BaseModel

class QueryHistory(BaseModel):
    """NL2SQL查询历史模型"""
    __tablename__ = "nl2sql_queries"
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    natural_language = Column(Text, nullable=False, comment="自然语言查询")
    generated_sql = Column(Text, nullable=True, comment="生成的SQL")
    execution_result = Column(Text, nullable=True, comment="执行结果JSON")
    is_success = Column(Boolean, nullable=True, comment="是否执行成功")
    error_message = Column(Text, nullable=True, comment="错误信息")
    execution_time_ms = Column(Integer, nullable=True, comment="执行耗时(毫秒)")
    is_favorite = Column(Boolean, default=False, comment="是否收藏")
    
    def __repr__(self):
        return f"<QueryHistory(user_id={self.user_id}, id={self.id})>"