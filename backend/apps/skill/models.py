from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from core.base_model import BaseModel

class AiSkill(BaseModel):
    """AI技能模型"""
    __tablename__ = "ai_skills"
    
    name = Column(String(100), nullable=False, comment="技能名称")
    code = Column(String(50), nullable=False, unique=True, comment="技能编码")
    description = Column(Text, nullable=True, comment="技能描述")
    prompt_template = Column(Text, nullable=False, comment="提示词模板")
    model_id = Column(Integer, ForeignKey("ai_models.id"), nullable=True, comment="关联模型ID")
    parameters = Column(Text, nullable=True, comment="参数配置JSON")
    is_active = Column(Boolean, default=True, comment="是否启用")
    category = Column(String(50), nullable=True, comment="分类")
    icon = Column(String(100), nullable=True, comment="图标")
    sort_order = Column(Integer, default=0, comment="排序")
    
    def __repr__(self):
        return f"<AiSkill(name={self.name}, id={self.id})>"