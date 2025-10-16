# 羲和API模块
from fastapi import APIRouter
from .v1 import api_router as v1_router

# 创建主API路由器
api_router = APIRouter()

# 包含v1版本的路由
api_router.include_router(v1_router, prefix="/api/v1")

__all__ = ["api_router"]