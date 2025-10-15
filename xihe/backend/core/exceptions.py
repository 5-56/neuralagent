"""
羲和自定义异常类
"""

from typing import Optional, Dict, Any


class XiheException(Exception):
    """羲和基础异常类"""
    
    def __init__(
        self,
        message: str,
        error_code: str = "XIHE_ERROR",
        status_code: int = 500,
        details: Optional[Dict[str, Any]] = None
    ):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        self.details = details or {}
        super().__init__(self.message)


class ValidationError(XiheException):
    """验证错误"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="VALIDATION_ERROR",
            status_code=400,
            details=details
        )


class AuthenticationError(XiheException):
    """认证错误"""
    
    def __init__(self, message: str = "认证失败", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AUTHENTICATION_ERROR",
            status_code=401,
            details=details
        )


class AuthorizationError(XiheException):
    """授权错误"""
    
    def __init__(self, message: str = "权限不足", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="AUTHORIZATION_ERROR",
            status_code=403,
            details=details
        )


class NotFoundError(XiheException):
    """资源未找到错误"""
    
    def __init__(self, message: str = "资源未找到", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="NOT_FOUND",
            status_code=404,
            details=details
        )


class AIProviderError(XiheException):
    """AI提供商错误"""
    
    def __init__(self, message: str, provider: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"AI提供商 {provider} 错误: {message}",
            error_code="AI_PROVIDER_ERROR",
            status_code=502,
            details=details
        )


class DesktopAutomationError(XiheException):
    """桌面自动化错误"""
    
    def __init__(self, message: str, action: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"桌面自动化错误 ({action}): {message}",
            error_code="DESKTOP_AUTOMATION_ERROR",
            status_code=500,
            details=details
        )


class SecurityError(XiheException):
    """安全错误"""
    
    def __init__(self, message: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="SECURITY_ERROR",
            status_code=403,
            details=details
        )


class RateLimitError(XiheException):
    """速率限制错误"""
    
    def __init__(self, message: str = "请求过于频繁", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_ERROR",
            status_code=429,
            details=details
        )