from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from common.database.session import get_db
from core.dependency import get_current_user
from .service import auth_service
from .schemas import UserRegister, UserLogin, TokenResponse, UserInfo, LoginResponse
from common.security.jwt import create_access_token
from .models import User

router = APIRouter()

@router.post("/register", response_model=UserInfo, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: AsyncSession = Depends(get_db)):
    """用户注册"""
    user, error = await auth_service.register(db, data)
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    return user

@router.post("/login", response_model=LoginResponse)
async def login(data: UserLogin, db: AsyncSession = Depends(get_db)):
    """用户登录"""
    user, error = await auth_service.login(db, data)
    if error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=error
        )
    
    # 创建访问令牌
    access_token = create_access_token({
        "user_id": user.id,
        "username": user.username
    })
    
    return LoginResponse(
        access_token=access_token,
        token_type="bearer",
        user=UserInfo.from_orm(user)
    )

@router.get("/me", response_model=UserInfo)
async def get_me(current_user: User = Depends(get_current_user)):
    """获取当前登录用户信息"""
    return current_user

@router.post("/logout")
async def logout():
    """用户登出"""
    # JWT是无状态的，前端清除token即可，后端不需要存储
    return {"message": "登出成功"}