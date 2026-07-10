from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import employee_service
from .schemas import EmployeeCreate, EmployeeUpdate, EmployeeList
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/employees", response_model=List[EmployeeList])
async def get_employees(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await employee_service.get_all(db, skip=skip, limit=limit)

@router.get("/employees/{id}", response_model=EmployeeList)
async def get_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = await employee_service.get_by_id(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="数字员工不存在")
    return employee

@router.post("/employees", response_model=EmployeeList, status_code=status.HTTP_201_CREATED)
async def create_employee(
    data: EmployeeCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await employee_service.create(db, {**data.dict(), "created_by": current_user.id})

@router.put("/employees/{id}", response_model=EmployeeList)
async def update_employee(
    id: int,
    data: EmployeeUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = await employee_service.update(db, id, data.dict(exclude_unset=True))
    if not employee:
        raise HTTPException(status_code=404, detail="数字员工不存在")
    return employee

@router.delete("/employees/{id}")
async def delete_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await employee_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="数字员工不存在")
    return {"message": "删除成功"}

@router.put("/employees/{id}/toggle", response_model=EmployeeList)
async def toggle_employee(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    employee = await employee_service.toggle_active(db, id)
    if not employee:
        raise HTTPException(status_code=404, detail="数字员工不存在")
    return employee