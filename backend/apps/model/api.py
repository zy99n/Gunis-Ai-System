from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import model_service
from .schemas import AiModelCreate, AiModelUpdate, AiModelList, TestResult
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/models", response_model=List[AiModelList])
async def get_models(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await model_service.get_all(db, skip=skip, limit=limit)

@router.get("/models/{id}", response_model=AiModelList)
async def get_model(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    model = await model_service.get_by_id(db, id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model

@router.post("/models", response_model=AiModelList, status_code=status.HTTP_201_CREATED)
async def create_model(
    data: AiModelCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    if data.is_default:
        await db.execute(
            model_service.model.__table__.update().where(
                model_service.model.is_default == True
            ).values(is_default=False)
        )
    return await model_service.create(db, data.dict())

@router.put("/models/{id}", response_model=AiModelList)
async def update_model(
    id: int,
    data: AiModelUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    update_data = data.dict(exclude_unset=True)
    if update_data.get("is_default"):
        await db.execute(
            model_service.model.__table__.update().where(
                model_service.model.is_default == True
            ).values(is_default=False)
        )
    model = await model_service.update(db, id, update_data)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model

@router.delete("/models/{id}")
async def delete_model(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await model_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="模型不存在")
    return {"message": "删除成功"}

@router.put("/models/{id}/default", response_model=AiModelList)
async def set_default_model(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    model = await model_service.set_default(db, id)
    if not model:
        raise HTTPException(status_code=404, detail="模型不存在")
    return model

@router.post("/models/{id}/test", response_model=TestResult)
async def test_model(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await model_service.test_connection(db, id)