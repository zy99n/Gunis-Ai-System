from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import Department, UserDepartment
from .schemas import DepartmentCreate, DepartmentUpdate, UserDepartmentCreate

class DepartmentService(BaseService[Department]):
    
    async def get_tree(self, db: AsyncSession) -> List[Dict[str, Any]]:
        """获取部门树形结构"""
        result = await db.execute(
            select(Department).where(
                Department.parent_id.is_(None),
                Department.is_deleted == False
            ).order_by(Department.sort_order)
        )
        root_departments = list(result.scalars().all())
        
        tree = []
        for dept in root_departments:
            tree.append(await self._build_tree_node(db, dept))
        
        return tree
    
    async def _build_tree_node(self, db: AsyncSession, dept: Department) -> Dict[str, Any]:
        """构建部门树节点"""
        result = await db.execute(
            select(Department).where(
                Department.parent_id == dept.id,
                Department.is_deleted == False
            ).order_by(Department.sort_order)
        )
        children = list(result.scalars().all())
        
        children_nodes = []
        for child in children:
            children_nodes.append(await self._build_tree_node(db, child))
        
        return {
            "id": dept.id,
            "name": dept.name,
            "parent_id": dept.parent_id,
            "sort_order": dept.sort_order,
            "description": dept.description,
            "is_deleted": dept.is_deleted,
            "created_at": dept.created_at,
            "updated_at": dept.updated_at,
            "children": children_nodes
        }
    
    async def move(self, db: AsyncSession, id: int, new_parent_id: Optional[int]) -> Optional[Department]:
        """移动部门到新的父部门下"""
        db_obj = await self.get_by_id(db, id)
        if not db_obj:
            return None
        
        if new_parent_id == id:
            return None
        
        if new_parent_id is not None:
            parent = await self.get_by_id(db, new_parent_id)
            if not parent:
                return None
        
        db_obj.parent_id = new_parent_id
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

class UserDepartmentService(BaseService[UserDepartment]):
    
    async def get_by_user_id(self, db: AsyncSession, user_id: int) -> List[UserDepartment]:
        """获取用户的部门关联"""
        result = await db.execute(
            select(UserDepartment).where(UserDepartment.user_id == user_id)
        )
        return list(result.scalars().all())
    
    async def get_by_department_id(self, db: AsyncSession, department_id: int) -> List[UserDepartment]:
        """获取部门下的用户"""
        result = await db.execute(
            select(UserDepartment).where(UserDepartment.department_id == department_id)
        )
        return list(result.scalars().all())
    
    async def create_or_update(self, db: AsyncSession, data: UserDepartmentCreate) -> UserDepartment:
        """创建或更新用户部门关联"""
        result = await db.execute(
            select(UserDepartment).where(
                UserDepartment.user_id == data.user_id,
                UserDepartment.department_id == data.department_id
            )
        )
        existing = result.scalar_one_or_none()
        
        if existing:
            existing.is_primary = data.is_primary
        else:
            existing = UserDepartment(
                user_id=data.user_id,
                department_id=data.department_id,
                is_primary=data.is_primary
            )
            db.add(existing)
        
        await db.commit()
        await db.refresh(existing)
        return existing

department_service = DepartmentService(Department)
user_department_service = UserDepartmentService(UserDepartment)