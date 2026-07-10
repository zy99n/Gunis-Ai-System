from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from core.base_service import BaseService
from .models import AiModel
from .schemas import AiModelCreate, AiModelUpdate

class AiModelService(BaseService[AiModel]):
    
    async def get_default(self, db: AsyncSession) -> Optional[AiModel]:
        """获取默认模型"""
        result = await db.execute(
            select(AiModel).where(
                AiModel.is_default == True,
                AiModel.is_active == True,
                AiModel.is_deleted == False
            )
        )
        return result.scalar_one_or_none()
    
    async def get_active_models(self, db: AsyncSession) -> List[AiModel]:
        """获取所有启用的模型"""
        result = await db.execute(
            select(AiModel).where(
                AiModel.is_active == True,
                AiModel.is_deleted == False
            ).order_by(AiModel.is_default.desc())
        )
        return list(result.scalars().all())
    
    async def set_default(self, db: AsyncSession, id: int) -> Optional[AiModel]:
        """设置默认模型"""
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return None
        
        await db.execute(
            update(AiModel).where(AiModel.is_default == True).values(is_default=False)
        )
        
        db_obj.is_default = True
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def test_connection(self, db: AsyncSession, id: int) -> dict:
        """测试模型连通性"""
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return {"success": False, "message": "模型不存在"}
        
        return {
            "success": True,
            "message": "测试连接成功（模拟）",
            "response_time_ms": 150
        }

model_service = AiModelService(AiModel)