from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from core.base_service import BaseService
from .models import User
from common.security.password import get_password_hash, verify_password
from common.security.jwt import create_access_token
from .schemas import UserRegister, UserLogin

class AuthService(BaseService[User]):
    """认证服务类"""
    
    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        result = await db.execute(
            select(User).where(User.username == username, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        result = await db.execute(
            select(User).where(User.email == email, User.is_deleted == False)
        )
        return result.scalar_one_or_none()
    
    async def get_user_by_username_or_email(
        self, db: AsyncSession, username_or_email: str
    ) -> Optional[User]:
        """根据用户名或邮箱获取用户"""
        user = await self.get_user_by_username(db, username_or_email)
        if not user:
            user = await self.get_user_by_email(db, username_or_email)
        return user
    
    async def register(
        self, db: AsyncSession, data: UserRegister
    ) -> Tuple[User | None, str]:
        """用户注册"""
        # 检查用户名是否已存在
        existing_user = await self.get_user_by_username(db, data.username)
        if existing_user:
            return None, "用户名已存在"
        
        # 检查邮箱是否已存在
        existing_email = await self.get_user_by_email(db, data.email)
        if existing_email:
            return None, "邮箱已被注册"
        
        # 创建用户
        user_data = {
            "username": data.username,
            "email": data.email,
            "password_hash": get_password_hash(data.password),
            "nickname": data.nickname or data.username,
        }
        user = await self.create(db, user_data)
        return user, ""
    
    async def login(
        self, db: AsyncSession, data: UserLogin
    ) -> Tuple[User | None, str | None]:
        """用户登录"""
        # 获取用户
        user = await self.get_user_by_username_or_email(db, data.username_or_email)
        if not user:
            return None, "用户名或密码错误"
        
        # 检查用户是否激活
        if not user.is_active:
            return None, "账号已被禁用"
        
        # 验证密码
        if not verify_password(data.password, user.password_hash):
            return None, "用户名或密码错误"
        
        return user, None

# 创建认证服务实例
auth_service = AuthService(User)