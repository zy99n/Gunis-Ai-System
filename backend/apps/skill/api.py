from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import skill_service
from .schemas import SkillCreate, SkillUpdate, SkillList, SkillGenerateRequest, TestResult
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/skills", response_model=List[SkillList])
async def get_skills(
    skip: int = 0,
    limit: int = 100,
    category: str = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if category:
        return await skill_service.get_by_category(db, category)
    return await skill_service.get_all(db, skip=skip, limit=limit)

@router.get("/skills/{id}", response_model=SkillList)
async def get_skill(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = await skill_service.get_by_id(db, id)
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    return skill

@router.post("/skills", response_model=SkillList, status_code=status.HTTP_201_CREATED)
async def create_skill(
    data: SkillCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await skill_service.create(db, data.dict())

@router.put("/skills/{id}", response_model=SkillList)
async def update_skill(
    id: int,
    data: SkillUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = await skill_service.update(db, id, data.dict(exclude_unset=True))
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    return skill

@router.delete("/skills/{id}")
async def delete_skill(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await skill_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="技能不存在")
    return {"message": "删除成功"}

@router.post("/skills/ai-generate", response_model=SkillList, status_code=status.HTTP_201_CREATED)
async def ai_generate_skill(
    data: SkillGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await skill_service.ai_generate(db, data)

@router.post("/skills/{id}/test", response_model=TestResult)
async def test_skill(
    id: int,
    test_input: str = "",
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await skill_service.test_skill(db, id, test_input)

@router.put("/skills/{id}/toggle", response_model=SkillList)
async def toggle_skill(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    skill = await skill_service.toggle_active(db, id)
    if not skill:
        raise HTTPException(status_code=404, detail="技能不存在")
    return skill