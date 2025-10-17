# 羲和API v1版本
from fastapi import APIRouter
from .auth import router as auth_router
from .users import router as users_router
from .tasks import router as tasks_router
from .agents import router as agents_router
from .workflows import router as workflows_router
from .conversations import router as conversations_router
from .files import router as files_router
from .desktop import router as desktop_router

# 创建v1 API路由器
api_router = APIRouter()

# 包含各个模块的路由
api_router.include_router(auth_router, prefix="/auth", tags=["认证"])
api_router.include_router(users_router, prefix="/users", tags=["用户"])
api_router.include_router(tasks_router, prefix="/tasks", tags=["任务"])
api_router.include_router(agents_router, prefix="/agents", tags=["AI代理"])
api_router.include_router(workflows_router, prefix="/workflows", tags=["工作流"])
api_router.include_router(conversations_router, prefix="/conversations", tags=["对话"])
api_router.include_router(files_router, prefix="/files", tags=["文件"])
api_router.include_router(desktop_router, prefix="/desktop", tags=["桌面自动化"])

__all__ = ["api_router"]