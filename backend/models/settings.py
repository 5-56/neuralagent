# 设置相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel

class SettingType(PyEnum):
    """设置类型枚举"""
    USER = "user"
    SYSTEM = "system"
    AI = "ai"
    DESKTOP = "desktop"
    VOICE = "voice"
    NOTIFICATION = "notification"
    SECURITY = "security"

class AppSettings(BaseModel):
    """应用设置模型"""
    __tablename__ = "app_settings"
    
    # 基本信息
    setting_key = Column(String(100), unique=True, nullable=False)
    setting_type = Column(Enum(SettingType), nullable=False)
    setting_name = Column(String(200), nullable=False)
    setting_description = Column(Text, nullable=True)
    
    # 设置值
    setting_value = Column(JSON, nullable=True)
    default_value = Column(JSON, nullable=True)
    
    # 配置信息
    is_required = Column(Boolean, default=False, nullable=False)
    is_encrypted = Column(Boolean, default=False, nullable=False)
    validation_rules = Column(JSON, nullable=True)
    
    # 状态信息
    is_active = Column(Boolean, default=True, nullable=False)
    is_readonly = Column(Boolean, default=False, nullable=False)
    
    # 版本信息
    version = Column(String(20), default="1.0.0", nullable=False)
    last_modified_by = Column(String(100), nullable=True)
    
    # 时间信息
    last_modified = Column(DateTime(timezone=True), nullable=True)