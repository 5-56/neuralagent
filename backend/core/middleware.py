# 中间件实现
import time
import logging
from typing import Callable
from fastapi import Request, Response
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp
import redis
from core.config import settings

logger = logging.getLogger(__name__)

# Redis连接（用于限流）
try:
    redis_client = redis.from_url(settings.REDIS_URL)
    redis_client.ping()
except Exception as e:
    logger.warning(f"Redis连接失败: {e}")
    redis_client = None

class LoggingMiddleware(BaseHTTPMiddleware):
    """日志中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("http")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # 记录请求开始时间
        start_time = time.time()
        
        # 记录请求信息
        self.logger.info(
            f"请求开始: {request.method} {request.url.path} "
            f"客户端: {request.client.host if request.client else 'unknown'}"
        )
        
        # 处理请求
        response = await call_next(request)
        
        # 计算处理时间
        process_time = time.time() - start_time
        
        # 记录响应信息
        self.logger.info(
            f"请求完成: {request.method} {request.url.path} "
            f"状态: {response.status_code} 耗时: {process_time:.3f}s"
        )
        
        # 添加响应头
        response.headers["X-Process-Time"] = str(process_time)
        
        return response

class RateLimitMiddleware(BaseHTTPMiddleware):
    """限流中间件"""
    
    def __init__(self, app: ASGIApp, calls: int = 100, period: int = 60):
        super().__init__(app)
        self.calls = calls
        self.period = period
        self.redis_client = redis_client
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        if not self.redis_client:
            # Redis不可用时跳过限流
            return await call_next(request)
        
        # 获取客户端IP
        client_ip = request.client.host if request.client else "unknown"
        
        # 构建限流键
        rate_limit_key = f"rate_limit:{client_ip}"
        
        try:
            # 检查当前请求数
            current_calls = self.redis_client.get(rate_limit_key)
            
            if current_calls is None:
                # 第一次请求
                self.redis_client.setex(rate_limit_key, self.period, 1)
            else:
                current_calls = int(current_calls)
                
                if current_calls >= self.calls:
                    # 超过限流阈值
                    logger.warning(f"客户端 {client_ip} 触发限流")
                    return JSONResponse(
                        status_code=429,
                        content={
                            "error": "RATE_LIMIT_EXCEEDED",
                            "message": "请求过于频繁，请稍后再试",
                            "retry_after": self.period
                        },
                        headers={"Retry-After": str(self.period)}
                    )
                else:
                    # 增加请求计数
                    self.redis_client.incr(rate_limit_key)
        
        except Exception as e:
            logger.error(f"限流检查失败: {e}")
            # Redis错误时允许请求通过
        
        return await call_next(request)

class CORSMiddleware:
    """CORS中间件"""
    
    def __init__(self, app: ASGIApp):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # 添加CORS头
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers = list(message.get("headers", []))
                    headers.extend([
                        [b"Access-Control-Allow-Origin", b"*"],
                        [b"Access-Control-Allow-Methods", b"GET, POST, PUT, DELETE, OPTIONS"],
                        [b"Access-Control-Allow-Headers", b"*"],
                        [b"Access-Control-Allow-Credentials", b"true"],
                    ])
                    message["headers"] = headers
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)

class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """错误处理中间件"""
    
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("error")
    
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            self.logger.error(f"未处理的异常: {e}", exc_info=True)
            
            return JSONResponse(
                status_code=500,
                content={
                    "error": "INTERNAL_SERVER_ERROR",
                    "message": "服务器内部错误",
                    "details": str(e) if settings.DEBUG else None
                }
            )