from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import crawler_service, etl_service
from .schemas import CrawlerTaskCreate, CrawlerTaskUpdate, CrawlerTaskList, EtlPipelineCreate, EtlPipelineUpdate, EtlPipelineList
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/crawler-tasks", response_model=List[CrawlerTaskList])
async def get_crawler_tasks(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crawler_service.get_all(db, skip=skip, limit=limit)

@router.get("/crawler-tasks/{id}", response_model=CrawlerTaskList)
async def get_crawler_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await crawler_service.get_by_id(db, id)
    if not task:
        raise HTTPException(status_code=404, detail="爬虫任务不存在")
    return task

@router.post("/crawler-tasks", response_model=CrawlerTaskList, status_code=status.HTTP_201_CREATED)
async def create_crawler_task(
    data: CrawlerTaskCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crawler_service.create(db, {**data.dict(), "created_by": current_user.id})

@router.put("/crawler-tasks/{id}", response_model=CrawlerTaskList)
async def update_crawler_task(
    id: int,
    data: CrawlerTaskUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    task = await crawler_service.update(db, id, data.dict(exclude_unset=True))
    if not task:
        raise HTTPException(status_code=404, detail="爬虫任务不存在")
    return task

@router.delete("/crawler-tasks/{id}")
async def delete_crawler_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await crawler_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="爬虫任务不存在")
    return {"message": "删除成功"}

@router.post("/crawler-tasks/{id}/run")
async def run_crawler_task(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await crawler_service.run(db, id)

@router.get("/etl-pipelines", response_model=List[EtlPipelineList])
async def get_etl_pipelines(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await etl_service.get_all(db, skip=skip, limit=limit)

@router.get("/etl-pipelines/{id}", response_model=EtlPipelineList)
async def get_etl_pipeline(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pipeline = await etl_service.get_by_id(db, id)
    if not pipeline:
        raise HTTPException(status_code=404, detail="ETL流水线不存在")
    return pipeline

@router.post("/etl-pipelines", response_model=EtlPipelineList, status_code=status.HTTP_201_CREATED)
async def create_etl_pipeline(
    data: EtlPipelineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await etl_service.create(db, {**data.dict(), "created_by": current_user.id})

@router.put("/etl-pipelines/{id}", response_model=EtlPipelineList)
async def update_etl_pipeline(
    id: int,
    data: EtlPipelineUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    pipeline = await etl_service.update(db, id, data.dict(exclude_unset=True))
    if not pipeline:
        raise HTTPException(status_code=404, detail="ETL流水线不存在")
    return pipeline

@router.delete("/etl-pipelines/{id}")
async def delete_etl_pipeline(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await etl_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="ETL流水线不存在")
    return {"message": "删除成功"}