from sqlalchemy import Column, Integer, String, Text, Boolean, DECIMAL
from core.base_model import BaseModel

class AiModel(BaseModel):
    """AI模型配置模型"""
    __tablename__ = "ai_models"
    
    name = Column(String(100), nullable=False, comment="模型名称")
    model_type = Column(String(50), nullable=False, comment="模型类型: openai, anthropic, google, baidu, aliyun, custom")
    api_base = Column(String(500), nullable=True, comment="API基础地址")
    api_key = Column(String(500), nullable=False, comment="API密钥")
    model_name = Column(String(100), nullable=False, comment="模型名称")
    temperature = Column(DECIMAL(3, 2), default=0.7, comment="温度参数")
    max_tokens = Column(Integer, default=2000, comment="最大token数")
    timeout = Column(Integer, default=30, comment="超时时间(秒)")
    is_default = Column(Boolean, default=False, comment="是否默认模型")
    is_active = Column(Boolean, default=True, comment="是否启用")
    description = Column(Text, nullable=True, comment="描述")
    
    def __repr__(self):
        return f"<AiModel(name={self.name}, id={self.id})>"