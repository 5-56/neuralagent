# 任务管理API
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.task import Task, TaskStatus, TaskPriority, TaskType
from schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskStepResponse
from services.task_service import TaskService

router = APIRouter()
task_service = TaskService()

@router.get("/", response_model=List[TaskResponse])
async def get_tasks(
    status: Optional[TaskStatus] = Query(None, description="任务状态筛选"),
    priority: Optional[TaskPriority] = Query(None, description="任务优先级筛选"),
    task_type: Optional[TaskType] = Query(None, description="任务类型筛选"),
    skip: int = Query(0, ge=0, description="跳过记录数"),
    limit: int = Query(100, ge=1, le=1000, description="限制记录数"),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取任务列表"""
    try:
        tasks = await task_service.get_tasks(
            db=db,
            user_id=current_user["user_id"],
            status=status,
            priority=priority,
            task_type=task_type,
            skip=skip,
            limit=limit
        )
        
        return [
            TaskResponse(
                id=task.id,
                title=task.title,
                description=task.description,
                task_type=task.task_type,
                status=task.status,
                priority=task.priority,
                progress=task.progress,
                started_at=task.started_at,
                completed_at=task.completed_at,
                estimated_duration=task.estimated_duration,
                config=task.config,
                input_data=task.input_data,
                output_data=task.output_data,
                error_message=task.error_message,
                retry_count=task.retry_count,
                execution_time=task.execution_time,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取任务列表失败: {str(e)}"
        )

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_data: TaskCreate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """创建新任务"""
    try:
        task = await task_service.create_task(
            db=db,
            user_id=current_user["user_id"],
            task_data=task_data
        )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            priority=task.priority,
            progress=task.progress,
            started_at=task.started_at,
            completed_at=task.completed_at,
            estimated_duration=task.estimated_duration,
            config=task.config,
            input_data=task.input_data,
            output_data=task.output_data,
            error_message=task.error_message,
            retry_count=task.retry_count,
            execution_time=task.execution_time,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"创建任务失败: {str(e)}"
        )

@router.get("/{task_id}", response_model=TaskResponse)
async def get_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取单个任务"""
    try:
        task = await task_service.get_task(db, task_id, current_user["user_id"])
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            priority=task.priority,
            progress=task.progress,
            started_at=task.started_at,
            completed_at=task.completed_at,
            estimated_duration=task.estimated_duration,
            config=task.config,
            input_data=task.input_data,
            output_data=task.output_data,
            error_message=task.error_message,
            retry_count=task.retry_count,
            execution_time=task.execution_time,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取任务失败: {str(e)}"
        )

@router.put("/{task_id}", response_model=TaskResponse)
async def update_task(
    task_id: int,
    task_data: TaskUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新任务"""
    try:
        task = await task_service.update_task(
            db=db,
            task_id=task_id,
            user_id=current_user["user_id"],
            task_data=task_data
        )
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        return TaskResponse(
            id=task.id,
            title=task.title,
            description=task.description,
            task_type=task.task_type,
            status=task.status,
            priority=task.priority,
            progress=task.progress,
            started_at=task.started_at,
            completed_at=task.completed_at,
            estimated_duration=task.estimated_duration,
            config=task.config,
            input_data=task.input_data,
            output_data=task.output_data,
            error_message=task.error_message,
            retry_count=task.retry_count,
            execution_time=task.execution_time,
            created_at=task.created_at,
            updated_at=task.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新任务失败: {str(e)}"
        )

@router.delete("/{task_id}")
async def delete_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除任务"""
    try:
        success = await task_service.delete_task(db, task_id, current_user["user_id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        return {"message": "任务删除成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除任务失败: {str(e)}"
        )

@router.post("/{task_id}/start")
async def start_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """启动任务"""
    try:
        success = await task_service.start_task(db, task_id, current_user["user_id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在或无法启动"
            )
        
        return {"message": "任务启动成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"启动任务失败: {str(e)}"
        )

@router.post("/{task_id}/pause")
async def pause_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """暂停任务"""
    try:
        success = await task_service.pause_task(db, task_id, current_user["user_id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在或无法暂停"
            )
        
        return {"message": "任务暂停成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"暂停任务失败: {str(e)}"
        )

@router.post("/{task_id}/cancel")
async def cancel_task(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """取消任务"""
    try:
        success = await task_service.cancel_task(db, task_id, current_user["user_id"])
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在或无法取消"
            )
        
        return {"message": "任务取消成功"}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"取消任务失败: {str(e)}"
        )

@router.get("/{task_id}/steps", response_model=List[TaskStepResponse])
async def get_task_steps(
    task_id: int,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取任务步骤"""
    try:
        steps = await task_service.get_task_steps(db, task_id, current_user["user_id"])
        if steps is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="任务不存在"
            )
        
        return [
            TaskStepResponse(
                id=step.id,
                task_id=step.task_id,
                step_name=step.step_name,
                step_description=step.step_description,
                step_order=step.step_order,
                status=step.status,
                progress=step.progress,
                action_type=step.action_type,
                action_config=step.action_config,
                input_data=step.input_data,
                output_data=step.output_data,
                started_at=step.started_at,
                completed_at=step.completed_at,
                execution_time=step.execution_time,
                error_message=step.error_message,
                created_at=step.created_at,
                updated_at=step.updated_at
            )
            for step in steps
        ]
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取任务步骤失败: {str(e)}"
        )