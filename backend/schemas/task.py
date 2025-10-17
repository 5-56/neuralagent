# 任务相关数据模式
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field
from models.task import TaskStatus, TaskPriority, TaskType

class TaskCreate(BaseModel):
    """任务创建"""
    title: str = Field(..., min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    task_type: TaskType = Field(TaskType.DESKTOP_AUTOMATION, description="任务类型")
    priority: TaskPriority = Field(TaskPriority.NORMAL, description="任务优先级")
    config: Optional[Dict[str, Any]] = Field(None, description="任务配置")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    estimated_duration: Optional[int] = Field(None, ge=1, description="预估执行时间（秒）")
    steps: Optional[List[Dict[str, Any]]] = Field(None, description="任务步骤")

class TaskUpdate(BaseModel):
    """任务更新"""
    title: Optional[str] = Field(None, min_length=1, max_length=200, description="任务标题")
    description: Optional[str] = Field(None, description="任务描述")
    priority: Optional[TaskPriority] = Field(None, description="任务优先级")
    config: Optional[Dict[str, Any]] = Field(None, description="任务配置")
    input_data: Optional[Dict[str, Any]] = Field(None, description="输入数据")
    estimated_duration: Optional[int] = Field(None, ge=1, description="预估执行时间（秒）")

class TaskResponse(BaseModel):
    """任务响应"""
    id: int
    title: str
    description: Optional[str]
    task_type: TaskType
    status: TaskStatus
    priority: TaskPriority
    progress: int
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    estimated_duration: Optional[int]
    config: Optional[Dict[str, Any]]
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    error_message: Optional[str]
    retry_count: int
    execution_time: Optional[int]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class TaskStepResponse(BaseModel):
    """任务步骤响应"""
    id: int
    task_id: int
    step_name: str
    step_description: Optional[str]
    step_order: int
    status: TaskStatus
    progress: int
    action_type: str
    action_config: Optional[Dict[str, Any]]
    input_data: Optional[Dict[str, Any]]
    output_data: Optional[Dict[str, Any]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    execution_time: Optional[int]
    error_message: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True