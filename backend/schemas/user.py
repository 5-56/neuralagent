# 用户相关数据模式
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field

class UserUpdate(BaseModel):
    """用户更新"""
    email: Optional[EmailStr] = Field(None, description="邮箱地址")
    display_name: Optional[str] = Field(None, max_length=100, description="显示名称")

class UserProfileResponse(BaseModel):
    """用户档案响应"""
    id: int
    user_id: int
    display_name: Optional[str]
    avatar_url: Optional[str]
    bio: Optional[str]
    language: str
    timezone: str
    theme: str
    total_tasks: int
    total_conversations: int
    total_workflows: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class UserSettingsResponse(BaseModel):
    """用户设置响应"""
    id: int
    user_id: int
    default_ai_provider: str
    default_ai_model: Optional[str]
    ai_temperature: str
    ai_max_tokens: str
    auto_screenshot: bool
    screenshot_interval: int
    auto_save_logs: bool
    voice_enabled: bool
    voice_language: str
    voice_speed: str
    voice_volume: str
    email_notifications: bool
    push_notifications: bool
    task_completion_notifications: bool
    two_factor_enabled: bool
    session_timeout: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True