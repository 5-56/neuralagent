# 用户相关数据模型
from sqlalchemy import Column, String, Boolean, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .base import BaseModel, SoftDeleteMixin

class User(BaseModel, SoftDeleteMixin):
    """用户模型"""
    __tablename__ = "users"
    
    # 基本信息
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    
    # 状态信息
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    is_superuser = Column(Boolean, default=False, nullable=False)
    
    # 时间信息
    last_login = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    settings = relationship("UserSettings", back_populates="user", uselist=False)
    tasks = relationship("Task", back_populates="user")
    conversations = relationship("Conversation", back_populates="user")
    workflows = relationship("Workflow", back_populates="user")

class UserProfile(BaseModel):
    """用户档案模型"""
    __tablename__ = "user_profiles"
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 个人信息
    display_name = Column(String(100), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    bio = Column(Text, nullable=True)
    
    # 偏好设置
    language = Column(String(10), default="zh-CN", nullable=False)
    timezone = Column(String(50), default="Asia/Shanghai", nullable=False)
    theme = Column(String(20), default="auto", nullable=False)  # light, dark, auto
    
    # 使用统计
    total_tasks = Column(Integer, default=0, nullable=False)
    total_conversations = Column(Integer, default=0, nullable=False)
    total_workflows = Column(Integer, default=0, nullable=False)
    
    # 关系
    user = relationship("User", back_populates="profile")

class UserSettings(BaseModel):
    """用户设置模型"""
    __tablename__ = "user_settings"
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # AI设置
    default_ai_provider = Column(String(50), default="openai", nullable=False)
    default_ai_model = Column(String(100), nullable=True)
    ai_temperature = Column(String(10), default="0.7", nullable=False)
    ai_max_tokens = Column(String(10), default="2048", nullable=False)
    
    # 桌面自动化设置
    auto_screenshot = Column(Boolean, default=True, nullable=False)
    screenshot_interval = Column(Integer, default=5, nullable=False)  # 秒
    auto_save_logs = Column(Boolean, default=True, nullable=False)
    
    # 语音设置
    voice_enabled = Column(Boolean, default=True, nullable=False)
    voice_language = Column(String(10), default="zh-CN", nullable=False)
    voice_speed = Column(String(10), default="1.0", nullable=False)
    voice_volume = Column(String(10), default="1.0", nullable=False)
    
    # 通知设置
    email_notifications = Column(Boolean, default=True, nullable=False)
    push_notifications = Column(Boolean, default=True, nullable=False)
    task_completion_notifications = Column(Boolean, default=True, nullable=False)
    
    # 安全设置
    two_factor_enabled = Column(Boolean, default=False, nullable=False)
    session_timeout = Column(Integer, default=3600, nullable=False)  # 秒
    
    # 关系
    user = relationship("User", back_populates="settings")