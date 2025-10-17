# 工作流相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel, SoftDeleteMixin

class WorkflowStatus(PyEnum):
    """工作流状态枚举"""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"

class WorkflowTriggerType(PyEnum):
    """工作流触发类型枚举"""
    MANUAL = "manual"
    SCHEDULED = "scheduled"
    EVENT = "event"
    API = "api"
    WEBHOOK = "webhook"

class WorkflowStepType(PyEnum):
    """工作流步骤类型枚举"""
    TASK = "task"
    CONDITION = "condition"
    LOOP = "loop"
    PARALLEL = "parallel"
    DELAY = "delay"
    NOTIFICATION = "notification"

class Workflow(BaseModel, SoftDeleteMixin):
    """工作流模型"""
    __tablename__ = "workflows"
    
    # 基本信息
    name = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    version = Column(String(20), default="1.0.0", nullable=False)
    
    # 状态信息
    status = Column(Enum(WorkflowStatus), default=WorkflowStatus.DRAFT, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # 触发配置
    trigger_type = Column(Enum(WorkflowTriggerType), default=WorkflowTriggerType.MANUAL, nullable=False)
    trigger_config = Column(JSON, nullable=True)
    
    # 工作流配置
    config = Column(JSON, nullable=True)
    variables = Column(JSON, nullable=True)  # 工作流变量
    
    # 统计信息
    execution_count = Column(Integer, default=0, nullable=False)
    success_count = Column(Integer, default=0, nullable=False)
    failure_count = Column(Integer, default=0, nullable=False)
    average_duration = Column(Integer, default=0, nullable=False)  # 平均执行时间（秒）
    
    # 时间信息
    last_executed = Column(DateTime(timezone=True), nullable=True)
    next_execution = Column(DateTime(timezone=True), nullable=True)
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    user = relationship("User", back_populates="workflows")
    steps = relationship("WorkflowStep", back_populates="workflow", cascade="all, delete-orphan")
    executions = relationship("WorkflowExecution", back_populates="workflow", cascade="all, delete-orphan")
    tasks = relationship("Task", back_populates="workflow")

class WorkflowStep(BaseModel):
    """工作流步骤模型"""
    __tablename__ = "workflow_steps"
    
    # 基本信息
    step_name = Column(String(200), nullable=False)
    step_description = Column(Text, nullable=True)
    step_type = Column(Enum(WorkflowStepType), nullable=False)
    step_order = Column(Integer, nullable=False)
    
    # 配置信息
    config = Column(JSON, nullable=True)
    conditions = Column(JSON, nullable=True)  # 条件配置
    actions = Column(JSON, nullable=True)  # 动作配置
    
    # 状态信息
    is_active = Column(Boolean, default=True, nullable=False)
    is_required = Column(Boolean, default=True, nullable=False)
    
    # 时间配置
    timeout = Column(Integer, nullable=True)  # 超时时间（秒）
    retry_count = Column(Integer, default=0, nullable=False)
    retry_delay = Column(Integer, default=0, nullable=False)  # 重试延迟（秒）
    
    # 外键
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    parent_step_id = Column(Integer, ForeignKey("workflow_steps.id"), nullable=True)
    
    # 关系
    workflow = relationship("Workflow", back_populates="steps")
    parent_step = relationship("WorkflowStep", remote_side="WorkflowStep.id")
    child_steps = relationship("WorkflowStep", back_populates="parent_step")

class WorkflowExecution(BaseModel):
    """工作流执行记录模型"""
    __tablename__ = "workflow_executions"
    
    # 基本信息
    execution_id = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(WorkflowStatus), nullable=False)
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    duration = Column(Integer, nullable=True)  # 执行时长（秒）
    
    # 配置信息
    config = Column(JSON, nullable=True)
    variables = Column(JSON, nullable=True)  # 执行时变量
    
    # 结果信息
    result_data = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # 统计信息
    steps_completed = Column(Integer, default=0, nullable=False)
    steps_failed = Column(Integer, default=0, nullable=False)
    total_steps = Column(Integer, default=0, nullable=False)
    
    # 外键
    workflow_id = Column(Integer, ForeignKey("workflows.id"), nullable=False)
    
    # 关系
    workflow = relationship("Workflow", back_populates="executions")