from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class QueryRequest(BaseModel):
    natural_language: str = Field(..., description="自然语言查询")

class QueryResponse(BaseModel):
    id: int
    natural_language: str
    generated_sql: Optional[str]
    execution_result: Optional[List[Dict[str, Any]]]
    is_success: bool
    error_message: Optional[str]
    execution_time_ms: Optional[int]
    created_at: str

class HistoryResponse(BaseModel):
    id: int
    natural_language: str
    generated_sql: Optional[str]
    is_success: Optional[bool]
    is_favorite: bool
    created_at: str
    
    class Config:
        from_attributes = True