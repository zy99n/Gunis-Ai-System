from pydantic import BaseModel, Field
from typing import Optional

class AiModelBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="模型名称")
    model_type: str = Field(..., description="模型类型")
    api_base: Optional[str] = Field(None, description="API基础地址")
    api_key: str = Field(..., description="API密钥")
    model_name: str = Field(..., description="模型名称")
    temperature: Optional[float] = Field(0.7, description="温度参数")
    max_tokens: Optional[int] = Field(2000, description="最大token数")
    timeout: Optional[int] = Field(30, description="超时时间(秒)")
    is_default: Optional[bool] = Field(False, description="是否默认模型")
    is_active: Optional[bool] = Field(True, description="是否启用")
    description: Optional[str] = Field(None, description="描述")

class AiModelCreate(AiModelBase):
    pass

class AiModelUpdate(AiModelBase):
    api_key: Optional[str] = Field(None, description="API密钥")

class AiModelList(BaseModel):
    id: int
    name: str
    model_type: str
    api_base: Optional[str]
    model_name: str
    temperature: float
    max_tokens: int
    timeout: int
    is_default: bool
    is_active: bool
    description: Optional[str]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class TestResult(BaseModel):
    success: bool
    message: str
    response_time_ms: Optional[int] = None