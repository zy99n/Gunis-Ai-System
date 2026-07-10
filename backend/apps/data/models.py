from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey, DateTime
from core.base_model import BaseModel

class CrawlerTask(BaseModel):
    """爬虫任务模型"""
    __tablename__ = "crawler_tasks"
    
    name = Column(String(100), nullable=False, comment="任务名称")
    url = Column(String(1000), nullable=False, comment="目标URL")
    crawler_type = Column(String(50), nullable=False, comment="爬虫类型: static, dynamic, api")
    selectors = Column(Text, nullable=True, comment="选择器配置JSON")
    headers = Column(Text, nullable=True, comment="请求头")
    interval_seconds = Column(Integer, default=3600, comment="执行间隔(秒)")
    max_retries = Column(Integer, default=3, comment="最大重试次数")
    timeout = Column(Integer, default=30, comment="超时时间(秒)")
    enabled = Column(Boolean, default=True, comment="是否启用")
    last_run_at = Column(DateTime, nullable=True, comment="上次运行时间")
    next_run_at = Column(DateTime, nullable=True, comment="下次运行时间")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    
    def __repr__(self):
        return f"<CrawlerTask(name={self.name}, id={self.id})>"

class EtlPipeline(BaseModel):
    """ETL流水线模型"""
    __tablename__ = "etl_pipelines"
    
    name = Column(String(100), nullable=False, comment="流水线名称")
    description = Column(Text, nullable=True, comment="描述")
    source_config = Column(Text, nullable=False, comment="数据源配置JSON")
    transform_config = Column(Text, nullable=True, comment="转换配置JSON")
    sink_config = Column(Text, nullable=False, comment="目标配置JSON")
    schedule_cron = Column(String(100), nullable=True, comment="定时表达式")
    enabled = Column(Boolean, default=True, comment="是否启用")
    created_by = Column(Integer, ForeignKey("users.id"), nullable=True, comment="创建人ID")
    
    def __repr__(self):
        return f"<EtlPipeline(name={self.name}, id={self.id})>"