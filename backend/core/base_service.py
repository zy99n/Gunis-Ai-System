from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from core.base_model import BaseModel

ModelType = TypeVar("ModelType", bound=BaseModel)

class BaseService(Generic[ModelType]):
    """基础服务类，提供通用CRUD操作"""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    async def get_by_id(self, db: AsyncSession, id: int) -> Optional[ModelType]:
        """根据ID获取"""
        result = await db.execute(
            select(self.model).where(self.model.id == id, self.model.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_all(self, db: AsyncSession, skip: int = 0, limit: int = 100) -> List[ModelType]:
        """获取所有列表"""
        result = await db.execute(
            select(self.model).where(self.model.is_deleted == False).offset(skip).limit(limit)
        )
        return list(result.scalars().all())
    
    async def create(self, db: AsyncSession, obj_in: Dict[str, Any]) -> ModelType:
        """创建"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj
    
    async def update(self, db: AsyncSession, id: int, obj_in: Dict[str, Any]) -> Optional[ModelType]:
        """更新"""
        stmt = update(self.model).where(self.model.id == id, self.model.is_deleted == False).values(**obj_in)
        await db.execute(stmt)
        await db.commit()
        return await self.get_by_id(db, id)
    
    async def delete(self, db: AsyncSession, id: int) -> bool:
        """软删除"""
        db_obj = await self.get_by_id(db, id)
        if db_obj:
            db_obj.soft_delete()
            await db.commit()
            return True
        return False
    
    async def hard_delete(self, db: AsyncSession, id: int) -> bool:
        """硬删除"""
        stmt = delete(self.model).where(self.model.id == id)
        result = await db.execute(stmt)
        await db.commit()
        return result.rowcount > 0