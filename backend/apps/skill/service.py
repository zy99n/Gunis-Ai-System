from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import AiSkill
from .schemas import SkillCreate, SkillUpdate, SkillGenerateRequest
import json

class SkillService(BaseService[AiSkill]):
    
    async def get_active_skills(self, db: AsyncSession) -> List[AiSkill]:
        """获取所有启用的技能"""
        result = await db.execute(
            select(AiSkill).where(
                AiSkill.is_active == True,
                AiSkill.is_deleted == False
            ).order_by(AiSkill.sort_order)
        )
        return list(result.scalars().all())
    
    async def get_by_category(self, db: AsyncSession, category: str) -> List[AiSkill]:
        """按分类获取技能"""
        result = await db.execute(
            select(AiSkill).where(
                AiSkill.category == category,
                AiSkill.is_active == True,
                AiSkill.is_deleted == False
            ).order_by(AiSkill.sort_order)
        )
        return list(result.scalars().all())
    
    async def ai_generate(self, db: AsyncSession, data: SkillGenerateRequest) -> AiSkill:
        """AI辅助生成技能（模拟）"""
        prompt_template = f"""
你是一个专业的{data.name}助手。
任务描述：{data.description}

请根据用户输入提供专业的回答。
"""
        
        return await self.create(db, {
            "name": data.name,
            "code": data.name.lower().replace(" ", "_"),
            "description": data.description,
            "prompt_template": prompt_template,
            "is_active": True,
            "sort_order": 0
        })
    
    async def test_skill(self, db: AsyncSession, id: int, test_input: str = "") -> dict:
        """测试技能（模拟）"""
        skill = await self.get_by_id(db, id)
        if not skill:
            return {"success": False, "message": "技能不存在"}
        
        return {
            "success": True,
            "message": "测试成功",
            "output": f"技能执行结果（模拟）：{skill.name} 处理了输入：{test_input or '默认测试输入'}"
        }
    
    async def toggle_active(self, db: AsyncSession, id: int) -> Optional[AiSkill]:
        """切换启用状态"""
        skill = await self.get_by_id(db, id)
        if not skill:
            return None
        
        skill.is_active = not skill.is_active
        await db.commit()
        await db.refresh(skill)
        return skill

skill_service = SkillService(AiSkill)