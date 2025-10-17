# AI代理相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel, SoftDeleteMixin

class AgentType(PyEnum):
    """代理类型枚举"""
    PLANNER = "planner"
    EXECUTOR = "executor"
    ANALYZER = "analyzer"
    COORDINATOR = "coordinator"
    MONITOR = "monitor"

class AgentStatus(PyEnum):
    """代理状态枚举"""
    IDLE = "idle"
    RUNNING = "running"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class MessageType(PyEnum):
    """消息类型枚举"""
    TEXT = "text"
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    FILE = "file"
    COMMAND = "command"
    RESPONSE = "response"
    ERROR = "error"

class Agent(BaseModel, SoftDeleteMixin):
    """AI代理模型"""
    __tablename__ = "agents"
    
    # 基本信息
    name = Column(String(100), nullable=False)
    agent_type = Column(Enum(AgentType), nullable=False)
    description = Column(Text, nullable=True)
    
    # 状态信息
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 配置信息
    ai_provider = Column(String(50), nullable=False)
    ai_model = Column(String(100), nullable=False)
    config = Column(JSON, nullable=True)
    
    # 能力信息
    capabilities = Column(JSON, nullable=True)  # 代理能力列表
    tools = Column(JSON, nullable=True)  # 可用工具列表
    
    # 统计信息
    total_sessions = Column(Integer, default=0, nullable=False)
    total_messages = Column(Integer, default=0, nullable=False)
    success_rate = Column(String(10), default="0.0", nullable=False)
    average_response_time = Column(Integer, default=0, nullable=False)  # 毫秒
    
    # 时间信息
    last_active = Column(DateTime(timezone=True), nullable=True)
    last_error = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    sessions = relationship("AgentSession", back_populates="agent", cascade="all, delete-orphan")

class AgentSession(BaseModel):
    """代理会话模型"""
    __tablename__ = "agent_sessions"
    
    # 基本信息
    session_id = Column(String(100), unique=True, nullable=False)
    title = Column(String(200), nullable=True)
    description = Column(Text, nullable=True)
    
    # 状态信息
    status = Column(Enum(AgentStatus), default=AgentStatus.IDLE, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 上下文信息
    context = Column(JSON, nullable=True)  # 会话上下文
    memory = Column(JSON, nullable=True)  # 会话记忆
    
    # 配置信息
    config = Column(JSON, nullable=True)
    
    # 统计信息
    message_count = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    cost = Column(String(20), default="0.00", nullable=False)
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True), nullable=True)
    last_activity = Column(DateTime(timezone=True), nullable=True)
    
    # 外键
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=True)
    
    # 关系
    agent = relationship("Agent", back_populates="sessions")
    messages = relationship("AgentMessage", back_populates="session", cascade="all, delete-orphan")

class AgentMessage(BaseModel):
    """代理消息模型"""
    __tablename__ = "agent_messages"
    
    # 基本信息
    message_type = Column(Enum(MessageType), nullable=False)
    content = Column(Text, nullable=False)
    
    # 角色信息
    role = Column(String(20), nullable=False)  # user, assistant, system
    sender = Column(String(100), nullable=True)  # 发送者
    
    # 元数据
    metadata = Column(JSON, nullable=True)
    attachments = Column(JSON, nullable=True)  # 附件信息
    
    # 处理信息
    processing_time = Column(Integer, nullable=True)  # 处理时间（毫秒）
    token_count = Column(Integer, nullable=True)  # token数量
    cost = Column(String(20), nullable=True)  # 成本
    
    # 状态信息
    is_processed = Column(Boolean, default=False, nullable=False)
    is_error = Column(Boolean, default=False, nullable=False)
    error_message = Column(Text, nullable=True)
    
    # 外键
    session_id = Column(Integer, ForeignKey("agent_sessions.id"), nullable=False)
    
    # 关系
    session = relationship("AgentSession", back_populates="messages")