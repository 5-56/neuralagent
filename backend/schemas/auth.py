# 认证相关数据模式
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class Token(BaseModel):
    """访问令牌"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(BaseModel):
    """令牌数据"""
    username: Optional[str] = None

class UserCreate(BaseModel):
    """用户创建"""
    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    email: EmailStr = Field(..., description="邮箱地址")
    password: str = Field(..., min_length=8, max_length=100, description="密码")
    display_name: Optional[str] = Field(None, max_length=100, description="显示名称")

class UserLogin(BaseModel):
    """用户登录"""
    username: str = Field(..., description="用户名或邮箱")
    password: str = Field(..., description="密码")
    remember_me: bool = Field(False, description="记住我")

class UserResponse(BaseModel):
    """用户响应"""
    id: int
    username: str
    email: str
    is_active: bool
    is_verified: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class PasswordReset(BaseModel):
    """密码重置"""
    email: EmailStr = Field(..., description="邮箱地址")

class PasswordResetConfirm(BaseModel):
    """密码重置确认"""
    token: str = Field(..., description="重置令牌")
    new_password: str = Field(..., min_length=8, max_length=100, description="新密码")

class EmailVerification(BaseModel):
    """邮箱验证"""
    token: str = Field(..., description="验证令牌")