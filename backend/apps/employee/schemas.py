from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class EmployeeBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="员工名称")
    avatar: Optional[str] = Field(None, description="头像")
    description: Optional[str] = Field(None, description="描述")
    model_id: Optional[int] = Field(None, description="默认模型ID")
    system_prompt: Optional[str] = Field(None, description="系统提示词")
    greeting: Optional[str] = Field(None, description="欢迎语")
    is_active: Optional[bool] = Field(True, description="是否启用")

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(EmployeeBase):
    name: Optional[str] = Field(None, description="员工名称")

class EmployeeList(BaseModel):
    id: int
    name: str
    avatar: Optional[str]
    description: Optional[str]
    model_id: Optional[int]
    is_active: bool
    created_by: Optional[int]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True