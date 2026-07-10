from typing import Optional, List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import QueryHistory
import json

class QueryService(BaseService[QueryHistory]):
    
    async def query(self, db: AsyncSession, user_id: int, natural_language: str) -> QueryHistory:
        """执行NL2SQL查询（模拟）"""
        generated_sql = f"SELECT * FROM users WHERE username LIKE '%{natural_language}%'"
        
        mock_result = [
            {"id": 1, "username": "admin", "email": "admin@example.com", "nickname": "管理员"},
            {"id": 2, "username": "testuser", "email": "test@example.com", "nickname": "测试用户"}
        ]
        
        query_record = await self.create(db, {
            "user_id": user_id,
            "natural_language": natural_language,
            "generated_sql": generated_sql,
            "execution_result": json.dumps(mock_result, ensure_ascii=False),
            "is_success": True,
            "execution_time_ms": 150
        })
        
        return query_record
    
    async def get_history(self, db: AsyncSession, user_id: int, skip: int = 0, limit: int = 50) -> List[QueryHistory]:
        """获取用户查询历史"""
        result = await db.execute(
            select(QueryHistory).where(
                QueryHistory.user_id == user_id
            ).order_by(QueryHistory.created_at.desc()).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def toggle_favorite(self, db: AsyncSession, id: int) -> Optional[QueryHistory]:
        """切换收藏状态"""
        record = await self.get_by_id(db, id)
        if not record:
            return None
        
        record.is_favorite = not record.is_favorite
        await db.commit()
        await db.refresh(record)
        return record

query_service = QueryService(QueryHistory)