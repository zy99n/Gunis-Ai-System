from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from core.base_model import BaseModel

class DigitalEmployee(BaseModel):
    """数字员工模型"""
    __tablename__ = "digital_employees"
    
    name = Column(String(100), nullable=False, comment="员工名称")
    avatar = Column(String(255), nullable=True, comment="头像")
    description = Column(Text, nullable=True, comment="描述")
    model_id = Column(Integer, ForeignKey("ai_models.id"), nullable=True, comment="默认模型ID")
    system_prompt = Column(Text, nullable=True, comment="系统提示词")
    greeting = Column(Text, nullable=True, comment="欢迎语")
    is_active = Column(Boolean, default=True, comment="是否启用")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    
    def __repr__(self):
        return f"<DigitalEmployee(name={self.name}, id={self.id})>"

class EmployeeSkill(BaseModel):
    """数字员工-技能关联模型"""
    __tablename__ = "employee_skill"
    
    employee_id = Column(Integer, ForeignKey("digital_employees.id"), nullable=False, comment="数字员工ID")
    skill_id = Column(Integer, ForeignKey("ai_skills.id"), nullable=False, comment="技能ID")
    sort_order = Column(Integer, default=0, comment="排序")
    config = Column(Text, nullable=True, comment="个性化配置")
    
    def __repr__(self):
        return f"<EmployeeSkill(employee_id={self.employee_id}, skill_id={self.skill_id})>"