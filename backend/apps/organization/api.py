from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import department_service, user_department_service
from .schemas import (
    DepartmentCreate, DepartmentUpdate, DepartmentTree, DepartmentList,
    UserDepartmentCreate, UserDepartmentUpdate, UserDepartmentResponse
)
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/departments/tree", response_model=List[DepartmentTree])
async def get_department_tree(db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):
    return await department_service.get_tree(db)

@router.get("/departments", response_model=List[DepartmentList])
async def get_departments(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await department_service.get_all(db, skip=skip, limit=limit)

@router.get("/departments/{id}", response_model=DepartmentList)
async def get_department(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = await department_service.get_by_id(db, id)
    if not dept:
        raise HTTPException(status_code=404, detail="部门不存在")
    return dept

@router.post("/departments", response_model=DepartmentList, status_code=status.HTTP_201_CREATED)
async def create_department(
    data: DepartmentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await department_service.create(db, data.dict())

@router.put("/departments/{id}", response_model=DepartmentList)
async def update_department(
    id: int,
    data: DepartmentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = await department_service.update(db, id, data.dict(exclude_unset=True))
    if not dept:
        raise HTTPException(status_code=404, detail="部门不存在")
    return dept

@router.delete("/departments/{id}")
async def delete_department(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await department_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"message": "删除成功"}

@router.put("/departments/{id}/move")
async def move_department(
    id: int,
    parent_id: int = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    dept = await department_service.move(db, id, parent_id)
    if not dept:
        raise HTTPException(status_code=404, detail="部门不存在")
    return {"message": "移动成功", "department": dept}

@router.get("/users/{user_id}/departments", response_model=List[UserDepartmentResponse])
async def get_user_departments(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    relations = await user_department_service.get_by_user_id(db, user_id)
    results = []
    for rel in relations:
        dept = await department_service.get_by_id(db, rel.department_id)
        results.append({
            "id": rel.id,
            "user_id": rel.user_id,
            "department_id": rel.department_id,
            "is_primary": rel.is_primary,
            "department_name": dept.name if dept else None
        })
    return results

@router.post("/users/{user_id}/departments", response_model=UserDepartmentResponse)
async def add_user_department(
    user_id: int,
    department_id: int,
    is_primary: bool = True,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    data = UserDepartmentCreate(user_id=user_id, department_id=department_id, is_primary=is_primary)
    rel = await user_department_service.create_or_update(db, data)
    dept = await department_service.get_by_id(db, rel.department_id)
    return {
        "id": rel.id,
        "user_id": rel.user_id,
        "department_id": rel.department_id,
        "is_primary": rel.is_primary,
        "department_name": dept.name if dept else None
    }

@router.delete("/users/{user_id}/departments/{department_id}")
async def remove_user_department(
    user_id: int,
    department_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        user_department_service.model.__table__.delete().where(
            user_department_service.model.user_id == user_id,
            user_department_service.model.department_id == department_id
        )
    )
    await db.commit()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="关联不存在")
    return {"message": "删除成功"}