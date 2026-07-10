from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import query_service
from .schemas import QueryRequest, QueryResponse, HistoryResponse
from apps.auth.models import User
from typing import List
import json

router = APIRouter()

@router.post("/query", response_model=QueryResponse)
async def execute_query(
    data: QueryRequest,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = await query_service.query(db, current_user.id, data.natural_language)
    result = {
        "id": record.id,
        "natural_language": record.natural_language,
        "generated_sql": record.generated_sql,
        "execution_result": json.loads(record.execution_result) if record.execution_result else None,
        "is_success": record.is_success,
        "error_message": record.error_message,
        "execution_time_ms": record.execution_time_ms,
        "created_at": record.created_at.isoformat() if record.created_at else ""
    }
    return result

@router.get("/history", response_model=List[HistoryResponse])
async def get_query_history(
    skip: int = 0,
    limit: int = 50,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return await query_service.get_history(db, current_user.id, skip=skip, limit=limit)

@router.post("/history/{id}/favorite", response_model=HistoryResponse)
async def toggle_favorite(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    record = await query_service.toggle_favorite(db, id)
    if not record:
        raise HTTPException(status_code=404, detail="记录不存在")
    return record

@router.delete("/history/{id}")
async def delete_history(
    id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = await query_service.delete(db, id)
    if not success:
        raise HTTPException(status_code=404, detail="记录不存在")
    return {"message": "删除成功"}