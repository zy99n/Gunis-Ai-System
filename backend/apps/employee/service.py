from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession
from core.base_service import BaseService
from .models import DigitalEmployee, EmployeeSkill

class EmployeeService(BaseService[DigitalEmployee]):
    
    async def toggle_active(self, db: AsyncSession, id: int) -> Optional[DigitalEmployee]:
        """切换启用状态"""
        employee = await self.get_by_id(db, id)
        if not employee:
            return None
        
        employee.is_active = not employee.is_active
        await db.commit()
        await db.refresh(employee)
        return employee

employee_service = EmployeeService(DigitalEmployee)