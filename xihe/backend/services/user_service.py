# 用户服务
from typing import Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import and_
from models.user import User, UserProfile, UserSettings
from schemas.user import UserUpdate
from services.auth_service import AuthService

class UserService:
    """用户服务"""
    
    def __init__(self):
        self.auth_service = AuthService()
    
    async def get_user_by_username(self, db: Session, username: str) -> Optional[User]:
        """根据用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    async def get_user_by_email(self, db: Session, email: str) -> Optional[User]:
        """根据邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    async def get_user_by_id(self, db: Session, user_id: int) -> Optional[User]:
        """根据ID获取用户"""
        return db.query(User).filter(User.id == user_id).first()
    
    async def update_user(self, db: Session, username: str, user_data: UserUpdate) -> Optional[User]:
        """更新用户信息"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        
        # 更新用户信息
        if user_data.email:
            user.email = user_data.email
        if user_data.display_name:
            # 更新或创建用户档案
            profile = await self.get_user_profile(db, username)
            if profile:
                profile.display_name = user_data.display_name
            else:
                profile = UserProfile(
                    user_id=user.id,
                    display_name=user_data.display_name
                )
                db.add(profile)
        
        db.commit()
        db.refresh(user)
        return user
    
    async def delete_user(self, db: Session, username: str) -> bool:
        """删除用户"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return False
        
        # 软删除
        user.is_deleted = True
        db.commit()
        return True
    
    async def get_user_profile(self, db: Session, username: str) -> Optional[UserProfile]:
        """获取用户档案"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        
        return db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    async def update_user_profile(self, db: Session, username: str, profile_data: Dict[str, Any]) -> Optional[UserProfile]:
        """更新用户档案"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        
        profile = await self.get_user_profile(db, username)
        if not profile:
            # 创建新档案
            profile = UserProfile(user_id=user.id)
            db.add(profile)
        
        # 更新档案信息
        for key, value in profile_data.items():
            if hasattr(profile, key):
                setattr(profile, key, value)
        
        db.commit()
        db.refresh(profile)
        return profile
    
    async def get_user_settings(self, db: Session, username: str) -> Optional[UserSettings]:
        """获取用户设置"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        
        return db.query(UserSettings).filter(UserSettings.user_id == user.id).first()
    
    async def update_user_settings(self, db: Session, username: str, settings_data: Dict[str, Any]) -> Optional[UserSettings]:
        """更新用户设置"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return None
        
        settings = await self.get_user_settings(db, username)
        if not settings:
            # 创建新设置
            settings = UserSettings(user_id=user.id)
            db.add(settings)
        
        # 更新设置信息
        for key, value in settings_data.items():
            if hasattr(settings, key):
                setattr(settings, key, value)
        
        db.commit()
        db.refresh(settings)
        return settings
    
    async def create_user_profile(self, db: Session, user_id: int, profile_data: Dict[str, Any]) -> UserProfile:
        """创建用户档案"""
        profile = UserProfile(user_id=user_id, **profile_data)
        db.add(profile)
        db.commit()
        db.refresh(profile)
        return profile
    
    async def create_user_settings(self, db: Session, user_id: int, settings_data: Dict[str, Any]) -> UserSettings:
        """创建用户设置"""
        settings = UserSettings(user_id=user_id, **settings_data)
        db.add(settings)
        db.commit()
        db.refresh(settings)
        return settings
    
    async def get_user_stats(self, db: Session, username: str) -> Dict[str, Any]:
        """获取用户统计信息"""
        user = await self.get_user_by_username(db, username)
        if not user:
            return {}
        
        profile = await self.get_user_profile(db, username)
        if not profile:
            return {
                "total_tasks": 0,
                "total_conversations": 0,
                "total_workflows": 0
            }
        
        return {
            "total_tasks": profile.total_tasks,
            "total_conversations": profile.total_conversations,
            "total_workflows": profile.total_workflows
        }
    
    async def update_user_stats(self, db: Session, username: str, stats_type: str, increment: int = 1) -> bool:
        """更新用户统计信息"""
        profile = await self.get_user_profile(db, username)
        if not profile:
            return False
        
        if stats_type == "tasks":
            profile.total_tasks += increment
        elif stats_type == "conversations":
            profile.total_conversations += increment
        elif stats_type == "workflows":
            profile.total_workflows += increment
        
        db.commit()
        return True