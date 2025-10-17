# 任务服务
from typing import List, Optional, Dict, Any
from datetime import datetime
from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from models.task import Task, TaskStep, TaskStatus, TaskPriority, TaskType
from schemas.task import TaskCreate, TaskUpdate
from services.agent_service import AgentService

class TaskService:
    """任务服务"""
    
    def __init__(self):
        self.agent_service = AgentService()
    
    async def get_tasks(
        self,
        db: Session,
        user_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        task_type: Optional[TaskType] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[Task]:
        """获取任务列表"""
        query = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.is_deleted == False
            )
        )
        
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        if task_type:
            query = query.filter(Task.task_type == task_type)
        
        return query.order_by(desc(Task.created_at)).offset(skip).limit(limit).all()
    
    async def get_task(self, db: Session, task_id: int, user_id: int) -> Optional[Task]:
        """获取单个任务"""
        return db.query(Task).filter(
            and_(
                Task.id == task_id,
                Task.user_id == user_id,
                Task.is_deleted == False
            )
        ).first()
    
    async def create_task(self, db: Session, user_id: int, task_data: TaskCreate) -> Task:
        """创建新任务"""
        task = Task(
            user_id=user_id,
            title=task_data.title,
            description=task_data.description,
            task_type=task_data.task_type,
            priority=task_data.priority,
            config=task_data.config,
            input_data=task_data.input_data,
            estimated_duration=task_data.estimated_duration
        )
        
        db.add(task)
        db.commit()
        db.refresh(task)
        
        # 创建任务步骤
        if task_data.steps:
            await self.create_task_steps(db, task.id, task_data.steps)
        
        return task
    
    async def update_task(
        self,
        db: Session,
        task_id: int,
        user_id: int,
        task_data: TaskUpdate
    ) -> Optional[Task]:
        """更新任务"""
        task = await self.get_task(db, task_id, user_id)
        if not task:
            return None
        
        # 更新任务信息
        for key, value in task_data.dict(exclude_unset=True).items():
            if hasattr(task, key):
                setattr(task, key, value)
        
        task.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(task)
        return task
    
    async def delete_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """删除任务"""
        task = await self.get_task(db, task_id, user_id)
        if not task:
            return False
        
        # 软删除
        task.is_deleted = True
        task.deleted_at = datetime.utcnow()
        db.commit()
        return True
    
    async def start_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """启动任务"""
        task = await self.get_task(db, task_id, user_id)
        if not task or task.status != TaskStatus.PENDING:
            return False
        
        task.status = TaskStatus.RUNNING
        task.started_at = datetime.utcnow()
        db.commit()
        
        # 异步执行任务
        # 这里应该启动任务执行器
        # await self.execute_task_async(task)
        
        return True
    
    async def pause_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """暂停任务"""
        task = await self.get_task(db, task_id, user_id)
        if not task or task.status != TaskStatus.RUNNING:
            return False
        
        task.status = TaskStatus.PAUSED
        db.commit()
        return True
    
    async def cancel_task(self, db: Session, task_id: int, user_id: int) -> bool:
        """取消任务"""
        task = await self.get_task(db, task_id, user_id)
        if not task or task.status in [TaskStatus.COMPLETED, TaskStatus.CANCELLED]:
            return False
        
        task.status = TaskStatus.CANCELLED
        task.completed_at = datetime.utcnow()
        db.commit()
        return True
    
    async def complete_task(self, db: Session, task_id: int, output_data: Dict[str, Any] = None) -> bool:
        """完成任务"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.utcnow()
        if output_data:
            task.output_data = output_data
        
        # 计算执行时间
        if task.started_at:
            task.execution_time = int((task.completed_at - task.started_at).total_seconds())
        
        db.commit()
        return True
    
    async def fail_task(self, db: Session, task_id: int, error_message: str, error_details: Dict[str, Any] = None) -> bool:
        """任务失败"""
        task = db.query(Task).filter(Task.id == task_id).first()
        if not task:
            return False
        
        task.status = TaskStatus.FAILED
        task.completed_at = datetime.utcnow()
        task.error_message = error_message
        if error_details:
            task.error_details = error_details
        
        # 计算执行时间
        if task.started_at:
            task.execution_time = int((task.completed_at - task.started_at).total_seconds())
        
        db.commit()
        return True
    
    async def create_task_steps(self, db: Session, task_id: int, steps_data: List[Dict[str, Any]]) -> List[TaskStep]:
        """创建任务步骤"""
        steps = []
        for i, step_data in enumerate(steps_data):
            step = TaskStep(
                task_id=task_id,
                step_name=step_data.get("step_name", f"步骤 {i + 1}"),
                step_description=step_data.get("step_description", ""),
                step_order=i + 1,
                action_type=step_data.get("action_type", "unknown"),
                action_config=step_data.get("action_config", {}),
                input_data=step_data.get("input_data")
            )
            db.add(step)
            steps.append(step)
        
        db.commit()
        for step in steps:
            db.refresh(step)
        
        return steps
    
    async def get_task_steps(self, db: Session, task_id: int, user_id: int) -> Optional[List[TaskStep]]:
        """获取任务步骤"""
        task = await self.get_task(db, task_id, user_id)
        if not task:
            return None
        
        return db.query(TaskStep).filter(TaskStep.task_id == task_id).order_by(TaskStep.step_order).all()
    
    async def update_task_step(
        self,
        db: Session,
        step_id: int,
        step_data: Dict[str, Any]
    ) -> Optional[TaskStep]:
        """更新任务步骤"""
        step = db.query(TaskStep).filter(TaskStep.id == step_id).first()
        if not step:
            return None
        
        for key, value in step_data.items():
            if hasattr(step, key):
                setattr(step, key, value)
        
        step.updated_at = datetime.utcnow()
        db.commit()
        db.refresh(step)
        return step
    
    async def execute_task_step(self, db: Session, step_id: int) -> bool:
        """执行任务步骤"""
        step = db.query(TaskStep).filter(TaskStep.id == step_id).first()
        if not step:
            return False
        
        try:
            step.status = TaskStatus.RUNNING
            step.started_at = datetime.utcnow()
            db.commit()
            
            # 使用代理服务执行步骤
            result = await self.agent_service.execute_task_step(step)
            
            if result.get("success", False):
                step.status = TaskStatus.COMPLETED
                step.output_data = result.get("output_data")
            else:
                step.status = TaskStatus.FAILED
                step.error_message = result.get("error", "执行失败")
            
            step.completed_at = datetime.utcnow()
            if step.started_at:
                step.execution_time = int((step.completed_at - step.started_at).total_seconds())
            
            db.commit()
            return True
            
        except Exception as e:
            step.status = TaskStatus.FAILED
            step.error_message = str(e)
            step.completed_at = datetime.utcnow()
            db.commit()
            return False
    
    async def get_task_statistics(self, db: Session, user_id: int) -> Dict[str, Any]:
        """获取任务统计信息"""
        total_tasks = db.query(Task).filter(
            and_(Task.user_id == user_id, Task.is_deleted == False)
        ).count()
        
        completed_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.is_deleted == False,
                Task.status == TaskStatus.COMPLETED
            )
        ).count()
        
        running_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.is_deleted == False,
                Task.status == TaskStatus.RUNNING
            )
        ).count()
        
        failed_tasks = db.query(Task).filter(
            and_(
                Task.user_id == user_id,
                Task.is_deleted == False,
                Task.status == TaskStatus.FAILED
            )
        ).count()
        
        return {
            "total": total_tasks,
            "completed": completed_tasks,
            "running": running_tasks,
            "failed": failed_tasks,
            "success_rate": (completed_tasks / total_tasks * 100) if total_tasks > 0 else 0
        }