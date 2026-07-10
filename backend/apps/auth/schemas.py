from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserRegister(BaseModel):
    """用户注册请求模型"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱")
    password: str = Field(..., min_length=6, max_length=20, description="密码")
    nickname: Optional[str] = Field(None, max_length=50, description="昵称")

class UserLogin(BaseModel):
    """用户登录请求模型"""
    username_or_email: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")

class TokenResponse(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str = "bearer"

class UserInfo(BaseModel):
    """用户信息响应模型"""
    id: int
    username: str
    email: str
    nickname: Optional[str]
    avatar: Optional[str]
    is_active: bool
    is_admin: bool
    
    class Config:
        from_attributes = True

class LoginResponse(BaseModel):
    """登录响应模型"""
    access_token: str
    token_type: str
    user: UserInfo