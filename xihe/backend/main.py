"""
羲和 (Xihe) - 智能化桌面助手后端服务
基于FastAPI构建的高性能AI代理后端
"""

import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.gzip import GZipMiddleware

from core.config import settings
from core.database import init_db
from core.security import setup_security
from api.v1.api import api_router
from core.exceptions import XiheException
from core.middleware import LoggingMiddleware, RateLimitMiddleware
from core.monitoring import setup_monitoring

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("xihe.log")
    ]
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """应用生命周期管理"""
    # 启动时执行
    logger.info("🚀 启动羲和后端服务...")
    
    # 初始化数据库
    await init_db()
    logger.info("✅ 数据库初始化完成")
    
    # 设置安全配置
    setup_security()
    logger.info("✅ 安全配置完成")
    
    # 设置监控
    setup_monitoring()
    logger.info("✅ 监控系统启动")
    
    yield
    
    # 关闭时执行
    logger.info("🛑 关闭羲和后端服务...")


# 创建FastAPI应用
app = FastAPI(
    title="羲和 (Xihe) - 智能化桌面助手",
    description="基于AI的智能化桌面自动化助手，支持多模态交互和广泛的AI提供商",
    version="1.0.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan
)

# 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(TrustedHostMiddleware, allowed_hosts=settings.ALLOWED_HOSTS)
app.add_middleware(GZipMiddleware, minimum_size=1000)
app.add_middleware(LoggingMiddleware)
app.add_middleware(RateLimitMiddleware)

# 静态文件服务
app.mount("/static", StaticFiles(directory="static"), name="static")

# 全局异常处理
@app.exception_handler(XiheException)
async def xihe_exception_handler(request: Request, exc: XiheException):
    """羲和自定义异常处理"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "message": exc.message,
            "details": exc.details
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """通用异常处理"""
    logger.error(f"未处理的异常: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "error": "INTERNAL_ERROR",
            "message": "服务器内部错误",
            "details": str(exc) if settings.DEBUG else None
        }
    )

# 健康检查
@app.get("/health")
async def health_check():
    """健康检查端点"""
    return {
        "status": "healthy",
        "service": "xihe-backend",
        "version": "1.0.0"
    }

# 根路径
@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "欢迎使用羲和 (Xihe) - 智能化桌面助手",
        "version": "1.0.0",
        "docs": "/docs" if settings.DEBUG else "文档已禁用"
    }

# 注册API路由
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level="info"
    )