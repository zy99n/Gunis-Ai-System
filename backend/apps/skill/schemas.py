from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class SkillBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="技能名称")
    code: str = Field(..., min_length=1, max_length=50, description="技能编码")
    description: Optional[str] = Field(None, description="技能描述")
    prompt_template: str = Field(..., description="提示词模板")
    model_id: Optional[int] = Field(None, description="关联模型ID")
    parameters: Optional[Dict[str, Any]] = Field(None, description="参数配置")
    is_active: Optional[bool] = Field(True, description="是否启用")
    category: Optional[str] = Field(None, description="分类")
    icon: Optional[str] = Field(None, description="图标")
    sort_order: Optional[int] = Field(0, description="排序")

class SkillCreate(SkillBase):
    pass

class SkillUpdate(SkillBase):
    name: Optional[str] = Field(None, description="技能名称")
    code: Optional[str] = Field(None, description="技能编码")
    prompt_template: Optional[str] = Field(None, description="提示词模板")

class SkillList(BaseModel):
    id: int
    name: str
    code: str
    description: Optional[str]
    model_id: Optional[int]
    is_active: bool
    category: Optional[str]
    icon: Optional[str]
    sort_order: int
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class SkillGenerateRequest(BaseModel):
    name: str = Field(..., description="技能名称")
    description: str = Field(..., description="技能描述")

class TestResult(BaseModel):
    success: bool
    message: str
    output: Optional[str] = None