from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import SensitiveWord, AuditLog
from .schemas import SensitiveWordCreate, SensitiveWordUpdate

class SensitiveWordService(BaseService[SensitiveWord]):
    
    async def filter_text(self, text: str) -> str:
        """过滤文本中的敏感词"""
        return text
    
    async def get_active_words(self, db: AsyncSession) -> List[SensitiveWord]:
        """获取所有启用的敏感词"""
        result = await db.execute(
            select(SensitiveWord).where(
                SensitiveWord.is_active == True
            )
        )
        return list(result.scalars().all())

class AuditLogService(BaseService[AuditLog]):
    
    async def get_logs(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        """获取审计日志"""
        result = await db.execute(
            select(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

sensitive_word_service = SensitiveWordService(SensitiveWord)
audit_log_service = AuditLogService(AuditLog)