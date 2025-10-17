# 对话相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel, SoftDeleteMixin

class ConversationType(PyEnum):
    """对话类型枚举"""
    CHAT = "chat"
    TASK_DISCUSSION = "task_discussion"
    WORKFLOW_DISCUSSION = "workflow_discussion"
    SUPPORT = "support"
    GENERAL = "general"

class MessageRole(PyEnum):
    """消息角色枚举"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"
    AGENT = "agent"

class MessageStatus(PyEnum):
    """消息状态枚举"""
    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"
    FAILED = "failed"

class Conversation(BaseModel, SoftDeleteMixin):
    """对话模型"""
    __tablename__ = "conversations"
    
    # 基本信息
    title = Column(String(200), nullable=True)
    conversation_type = Column(Enum(ConversationType), default=ConversationType.CHAT, nullable=False)
    
    # 状态信息
    is_active = Column(Boolean, default=True, nullable=False)
    is_archived = Column(Boolean, default=False, nullable=False)
    
    # 配置信息
    config = Column(JSON, nullable=True)
    context = Column(JSON, nullable=True)  # 对话上下文
    
    # 统计信息
    message_count = Column(Integer, default=0, nullable=False)
    total_tokens = Column(Integer, default=0, nullable=False)
    cost = Column(String(20), default="0.00", nullable=False)
    
    # 时间信息
    last_message_at = Column(DateTime(timezone=True), nullable=True)
    last_read_at = Column(DateTime(timezone=True), nullable=True)
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    agent_id = Column(Integer, ForeignKey("agents.id"), nullable=True)
    
    # 关系
    user = relationship("User", back_populates="conversations")
    agent = relationship("Agent")
    messages = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(BaseModel):
    """消息模型"""
    __tablename__ = "messages"
    
    # 基本信息
    content = Column(Text, nullable=False)
    role = Column(Enum(MessageRole), nullable=False)
    message_type = Column(String(50), default="text", nullable=False)
    
    # 状态信息
    status = Column(Enum(MessageStatus), default=MessageStatus.SENT, nullable=False)
    is_edited = Column(Boolean, default=False, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    
    # 元数据
    metadata = Column(JSON, nullable=True)
    attachments = Column(JSON, nullable=True)  # 附件信息
    
    # 处理信息
    processing_time = Column(Integer, nullable=True)  # 处理时间（毫秒）
    token_count = Column(Integer, nullable=True)  # token数量
    cost = Column(String(20), nullable=True)  # 成本
    
    # 编辑信息
    edited_at = Column(DateTime(timezone=True), nullable=True)
    edit_reason = Column(String(200), nullable=True)
    
    # 外键
    conversation_id = Column(Integer, ForeignKey("conversations.id"), nullable=False)
    parent_message_id = Column(Integer, ForeignKey("messages.id"), nullable=True)
    
    # 关系
    conversation = relationship("Conversation", back_populates="messages")
    parent_message = relationship("Message", remote_side="Message.id")
    replies = relationship("Message", back_populates="parent_message")