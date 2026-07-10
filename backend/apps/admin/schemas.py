from pydantic import BaseModel, Field
from typing import Optional

class SensitiveWordCreate(BaseModel):
    word: str = Field(..., min_length=1, max_length=100, description="敏感词")
    category: Optional[str] = Field(None, description="分类")
    replacement: Optional[str] = Field("*", description="替换字符")
    is_active: Optional[bool] = Field(True, description="是否启用")

class SensitiveWordUpdate(BaseModel):
    category: Optional[str] = Field(None, description="分类")
    replacement: Optional[str] = Field(None, description="替换字符")
    is_active: Optional[bool] = Field(None, description="是否启用")

class SensitiveWordList(BaseModel):
    id: int
    word: str
    category: Optional[str]
    replacement: str
    is_active: bool
    created_at: str
    
    class Config:
        from_attributes = True

class AuditLogQuery(BaseModel):
    user_id: Optional[int] = None
    module: Optional[str] = None
    action: Optional[str] = None
    status: Optional[str] = None

class AuditLogList(BaseModel):
    id: int
    user_id: Optional[int]
    username: Optional[str]
    action: str
    module: Optional[str]
    description: Optional[str]
    request_ip: Optional[str]
    status: Optional[str]
    created_at: str
    
    class Config:
        from_attributes = True