from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class CrawlerTaskBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="任务名称")
    url: str = Field(..., description="目标URL")
    crawler_type: str = Field(..., description="爬虫类型")
    selectors: Optional[Dict[str, Any]] = Field(None, description="选择器配置")
    headers: Optional[Dict[str, Any]] = Field(None, description="请求头")
    interval_seconds: Optional[int] = Field(3600, description="执行间隔(秒)")
    max_retries: Optional[int] = Field(3, description="最大重试次数")
    timeout: Optional[int] = Field(30, description="超时时间(秒)")
    enabled: Optional[bool] = Field(True, description="是否启用")

class CrawlerTaskCreate(CrawlerTaskBase):
    pass

class CrawlerTaskUpdate(CrawlerTaskBase):
    name: Optional[str] = Field(None, description="任务名称")
    url: Optional[str] = Field(None, description="目标URL")

class CrawlerTaskList(BaseModel):
    id: int
    name: str
    url: str
    crawler_type: str
    interval_seconds: int
    enabled: bool
    last_run_at: Optional[str]
    next_run_at: Optional[str]
    created_by: Optional[int]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True

class EtlPipelineBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="流水线名称")
    description: Optional[str] = Field(None, description="描述")
    source_config: Dict[str, Any] = Field(..., description="数据源配置")
    transform_config: Optional[Dict[str, Any]] = Field(None, description="转换配置")
    sink_config: Dict[str, Any] = Field(..., description="目标配置")
    schedule_cron: Optional[str] = Field(None, description="定时表达式")
    enabled: Optional[bool] = Field(True, description="是否启用")

class EtlPipelineCreate(EtlPipelineBase):
    pass

class EtlPipelineUpdate(EtlPipelineBase):
    name: Optional[str] = Field(None, description="流水线名称")
    source_config: Optional[Dict[str, Any]] = Field(None, description="数据源配置")
    sink_config: Optional[Dict[str, Any]] = Field(None, description="目标配置")

class EtlPipelineList(BaseModel):
    id: int
    name: str
    description: Optional[str]
    schedule_cron: Optional[str]
    enabled: bool
    created_by: Optional[int]
    created_at: str
    updated_at: str
    
    class Config:
        from_attributes = True