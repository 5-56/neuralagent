# 安全配置和中间件
import logging
from typing import Optional
from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from core.config import settings
from services.auth_service import AuthService

logger = logging.getLogger(__name__)

# 创建认证服务实例
auth_service = AuthService()

# HTTP Bearer 认证
security = HTTPBearer()

def setup_security():
    """设置安全配置"""
    logger.info("安全配置已启用")
    
    # 验证必要的安全配置
    if not settings.SECRET_KEY:
        raise ValueError("SECRET_KEY 未设置")
    
    if not settings.ENCRYPTION_KEY:
        raise ValueError("ENCRYPTION_KEY 未设置")
    
    logger.info(f"安全级别: {settings.SECURITY_LEVEL}")
    logger.info(f"最大文件大小: {settings.MAX_FILE_SIZE / 1024 / 1024:.1f}MB")
    logger.info(f"允许的文件类型: {len(settings.ALLOWED_FILE_TYPES)} 种")

async def get_current_user(credentials: HTTPAuthorizationCredentials = security):
    """获取当前用户"""
    try:
        token = credentials.credentials
        token_data = auth_service.verify_access_token(token)
        
        # 这里应该从数据库获取用户信息
        # 暂时返回模拟用户
        return {
            "username": token_data.username,
            "is_authenticated": True
        }
        
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的认证令牌",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"用户认证失败: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="认证失败",
            headers={"WWW-Authenticate": "Bearer"},
        )

def verify_file_type(content_type: str) -> bool:
    """验证文件类型"""
    return content_type in settings.ALLOWED_FILE_TYPES

def verify_file_size(file_size: int) -> bool:
    """验证文件大小"""
    return file_size <= settings.MAX_FILE_SIZE

def get_security_headers() -> dict:
    """获取安全头"""
    headers = {
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "DENY",
        "X-XSS-Protection": "1; mode=block",
        "Referrer-Policy": "strict-origin-when-cross-origin"
    }
    
    if settings.SECURITY_LEVEL == "high":
        headers.update({
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'"
        })
    
    return headers

class SecurityMiddleware:
    """安全中间件"""
    
    def __init__(self, app):
        self.app = app
    
    async def __call__(self, scope, receive, send):
        if scope["type"] == "http":
            # 添加安全头
            headers = get_security_headers()
            
            async def send_wrapper(message):
                if message["type"] == "http.response.start":
                    headers_list = list(message.get("headers", []))
                    for key, value in headers.items():
                        headers_list.append([key.encode(), value.encode()])
                    message["headers"] = headers_list
                await send(message)
            
            await self.app(scope, receive, send_wrapper)
        else:
            await self.app(scope, receive, send)