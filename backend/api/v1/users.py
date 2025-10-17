# 用户管理API
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from core.database import get_db
from core.security import get_current_user
from models.user import User, UserProfile, UserSettings
from schemas.user import UserResponse, UserUpdate, UserProfileResponse, UserSettingsResponse
from services.user_service import UserService

router = APIRouter()
user_service = UserService()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取当前用户信息"""
    try:
        user = await user_service.get_user_by_username(db, current_user["username"])
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户不存在"
            )
        
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户信息失败: {str(e)}"
        )

@router.put("/me", response_model=UserResponse)
async def update_current_user(
    user_update: UserUpdate,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新当前用户信息"""
    try:
        user = await user_service.update_user(db, current_user["username"], user_update)
        return UserResponse(
            id=user.id,
            username=user.username,
            email=user.email,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户信息失败: {str(e)}"
        )

@router.get("/me/profile", response_model=UserProfileResponse)
async def get_user_profile(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户档案"""
    try:
        profile = await user_service.get_user_profile(db, current_user["username"])
        if not profile:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户档案不存在"
            )
        
        return UserProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            display_name=profile.display_name,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            language=profile.language,
            timezone=profile.timezone,
            theme=profile.theme,
            total_tasks=profile.total_tasks,
            total_conversations=profile.total_conversations,
            total_workflows=profile.total_workflows,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户档案失败: {str(e)}"
        )

@router.put("/me/profile", response_model=UserProfileResponse)
async def update_user_profile(
    profile_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户档案"""
    try:
        profile = await user_service.update_user_profile(db, current_user["username"], profile_data)
        return UserProfileResponse(
            id=profile.id,
            user_id=profile.user_id,
            display_name=profile.display_name,
            avatar_url=profile.avatar_url,
            bio=profile.bio,
            language=profile.language,
            timezone=profile.timezone,
            theme=profile.theme,
            total_tasks=profile.total_tasks,
            total_conversations=profile.total_conversations,
            total_workflows=profile.total_workflows,
            created_at=profile.created_at,
            updated_at=profile.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户档案失败: {str(e)}"
        )

@router.get("/me/settings", response_model=UserSettingsResponse)
async def get_user_settings(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """获取用户设置"""
    try:
        settings = await user_service.get_user_settings(db, current_user["username"])
        if not settings:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="用户设置不存在"
            )
        
        return UserSettingsResponse(
            id=settings.id,
            user_id=settings.user_id,
            default_ai_provider=settings.default_ai_provider,
            default_ai_model=settings.default_ai_model,
            ai_temperature=settings.ai_temperature,
            ai_max_tokens=settings.ai_max_tokens,
            auto_screenshot=settings.auto_screenshot,
            screenshot_interval=settings.screenshot_interval,
            auto_save_logs=settings.auto_save_logs,
            voice_enabled=settings.voice_enabled,
            voice_language=settings.voice_language,
            voice_speed=settings.voice_speed,
            voice_volume=settings.voice_volume,
            email_notifications=settings.email_notifications,
            push_notifications=settings.push_notifications,
            task_completion_notifications=settings.task_completion_notifications,
            two_factor_enabled=settings.two_factor_enabled,
            session_timeout=settings.session_timeout,
            created_at=settings.created_at,
            updated_at=settings.updated_at
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"获取用户设置失败: {str(e)}"
        )

@router.put("/me/settings", response_model=UserSettingsResponse)
async def update_user_settings(
    settings_data: dict,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """更新用户设置"""
    try:
        settings = await user_service.update_user_settings(db, current_user["username"], settings_data)
        return UserSettingsResponse(
            id=settings.id,
            user_id=settings.user_id,
            default_ai_provider=settings.default_ai_provider,
            default_ai_model=settings.default_ai_model,
            ai_temperature=settings.ai_temperature,
            ai_max_tokens=settings.ai_max_tokens,
            auto_screenshot=settings.auto_screenshot,
            screenshot_interval=settings.screenshot_interval,
            auto_save_logs=settings.auto_save_logs,
            voice_enabled=settings.voice_enabled,
            voice_language=settings.voice_language,
            voice_speed=settings.voice_speed,
            voice_volume=settings.voice_volume,
            email_notifications=settings.email_notifications,
            push_notifications=settings.push_notifications,
            task_completion_notifications=settings.task_completion_notifications,
            two_factor_enabled=settings.two_factor_enabled,
            session_timeout=settings.session_timeout,
            created_at=settings.created_at,
            updated_at=settings.updated_at
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"更新用户设置失败: {str(e)}"
        )

@router.delete("/me")
async def delete_current_user(
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """删除当前用户"""
    try:
        await user_service.delete_user(db, current_user["username"])
        return {"message": "用户删除成功"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"删除用户失败: {str(e)}"
        )