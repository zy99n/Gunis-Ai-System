from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import sensitive_word_service, audit_log_service
from .schemas import SensitiveWordCreate, SensitiveWordUpdate, SensitiveWordList, AuditLogList
from apps.auth.models import User
from typing import List

router = APIRouter()

@router.get("/sensitive-words", response_model=List[SensitiveWordList])
async def get_sensitive_words(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await sensitive_word_service.get_all(db, skip=skip, limit=limit)

@router.post("/sensitive-words", response_model=SensitiveWordList, status_code=status.HTTP_201_CREATED)
async def create_sensitive_word(
    data: SensitiveWordCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await sensitive_word_service.create(db, data.dict())

@router.put("/sensitive-words/{id}", response_model=SensitiveWordList)
async def update_sensitive_word(
    id: int,
    data: SensitiveWordUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    word = await sensitive_word_service.update(db, id, data.dict(exclude_unset=True))
    if not word:
        raise HTTPException(status_code=404, detail="敏感词不存在")
    return word

@router.delete("/sensitive-words/{id}")
async def delete_sensitive_word(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await sensitive_word_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="敏感词不存在")
    return {"message": "删除成功"}

@router.get("/audit-logs", response_model=List[AuditLogList])
async def get_audit_logs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await audit_log_service.get_logs(db, skip=skip, limit=limit)