"""
羲和配置管理
支持环境变量和配置文件
"""

import os
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class Settings(BaseModel):
    """应用配置"""
    
    # 基础配置
    APP_NAME: str = "羲和 (Xihe)"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    SECRET_KEY: str
    
    # 服务器配置
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # 数据库配置
    DATABASE_URL: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20
    
    # Redis配置
    REDIS_URL: str = "redis://localhost:6379"
    
    # JWT配置
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    JWT_REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # AI提供商配置
    # OpenAI
    OPENAI_API_KEY: Optional[str] = None
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    OPENAI_MODEL: str = "gpt-4"
    
    # Anthropic
    ANTHROPIC_API_KEY: Optional[str] = None
    ANTHROPIC_MODEL: str = "claude-3-sonnet-20240229"
    
    # Google Gemini
    GOOGLE_API_KEY: Optional[str] = None
    GOOGLE_MODEL: str = "gemini-pro"
    
    # Azure OpenAI
    AZURE_OPENAI_ENDPOINT: Optional[str] = None
    AZURE_OPENAI_API_KEY: Optional[str] = None
    AZURE_OPENAI_API_VERSION: str = "2024-02-15-preview"
    AZURE_OPENAI_DEPLOYMENT: str = "gpt-4"
    
    # AWS Bedrock
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    BEDROCK_MODEL: str = "anthropic.claude-3-sonnet-20240229-v1:0"
    
    # 本地模型
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "llama2"
    
    # 语音配置
    SPEECH_RECOGNITION_LANGUAGE: str = "zh-CN"
    SPEECH_SYNTHESIS_VOICE: str = "zh-CN-XiaoxiaoNeural"
    
    # 安全配置
    SECURITY_LEVEL: str = "medium"  # low, medium, high
    ENCRYPTION_KEY: str
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_FILE_TYPES: List[str] = [
        "image/jpeg", "image/png", "image/gif",
        "application/pdf", "text/plain",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ]
    
    # 监控配置
    ENABLE_METRICS: bool = True
    METRICS_PORT: int = 9090
    
    # 日志配置
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "xihe.log"
    
    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @field_validator("SECURITY_LEVEL")
    @classmethod
    def validate_security_level(cls, v):
        if v not in ["low", "medium", "high"]:
            raise ValueError("安全级别必须是 low, medium 或 high")
        return v
    
    model_config = {
        "env_file": ".env",
        "case_sensitive": True
    }


# 创建全局设置实例
settings = Settings()