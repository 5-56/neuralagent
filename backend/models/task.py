# 任务相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel, SoftDeleteMixin

class TaskStatus(PyEnum):
    """任务状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class TaskPriority(PyEnum):
    """任务优先级枚举"""
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class TaskType(PyEnum):
    """任务类型枚举"""
    DESKTOP_AUTOMATION = "desktop_automation"
    WEB_AUTOMATION = "web_automation"
    FILE_PROCESSING = "file_processing"
    DATA_ANALYSIS = "data_analysis"
    COMMUNICATION = "communication"
    CUSTOM = "custom"

class Task(BaseModel, SoftDeleteMixin):
    """任务模型"""
    __tablename__ = "tasks"
    
    # 基本信息
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    task_type = Column(Enum(TaskType), default=TaskType.DESKTOP_AUTOMATION, nullable=False)
    
    # 状态信息
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    priority = Column(Enum(TaskPriority), default=TaskPriority.NORMAL, nullable=False)
    progress = Column(Integer, default=0, nullable=False)  # 0-100
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    estimated_duration = Column(Integer, nullable=True)  # 秒
    
    # 配置信息
    config = Column(JSON, nullable=True)  # 任务配置
    input_data = Column(JSON, nullable=True)  # 输入数据
    output_data = Column(JSON, nullable=True)  # 输出数据
    
    # 错误信息
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # 统计信息
    retry_count = Column(Integer, default=0, nullable=False)
    execution_time = Column(Integer, nullable=True)  # 实际执行时间（秒）
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=True)
    
    # 关系
    user = relationship("User", back_populates="tasks")
    workflow = relationship("Workflow", back_populates="tasks")
    steps = relationship("TaskStep", back_populates="task", cascade="all, delete-orphan")
    executions = relationship("TaskExecution", back_populates="task", cascade="all, delete-orphan")

class TaskStep(BaseModel):
    """任务步骤模型"""
    __tablename__ = "task_steps"
    
    # 基本信息
    step_name = Column(String(200), nullable=False)
    step_description = Column(Text, nullable=True)
    step_order = Column(Integer, nullable=False)
    
    # 状态信息
    status = Column(Enum(TaskStatus), default=TaskStatus.PENDING, nullable=False)
    progress = Column(Integer, default=0, nullable=False)
    
    # 配置信息
    action_type = Column(String(50), nullable=False)  # click, type, scroll, etc.
    action_config = Column(JSON, nullable=True)
    input_data = Column(JSON, nullable=True)
    output_data = Column(JSON, nullable=True)
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=True)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    execution_time = Column(Integer, nullable=True)
    
    # 错误信息
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # 外键
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    
    # 关系
    task = relationship("Task", back_populates="steps")

class TaskExecution(BaseModel):
    """任务执行记录模型"""
    __tablename__ = "task_executions"
    
    # 基本信息
    execution_id = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(TaskStatus), nullable=False)
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # 执行时长（秒）
    
    # 环境信息
    environment = Column(JSON, nullable=True)  # 执行环境信息
    system_info = Column(JSON, nullable=True)  # 系统信息
    
    # 结果信息
    result_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # 统计信息
    steps_completed = Column(Integer, default=0, nullable=False)
    steps_failed = Column(Integer, default=0, nullable=False)
    total_steps = Column(Integer, default=0, nullable=False)
    
    # 外键
    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    
    # 关系
    task = relationship("Task", back_populates="executions")