# 自定义异常类
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

class ConflictError(XiheException):
    """冲突错误"""
    
    def __init__(self, message: str = "资源冲突", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="CONFLICT_ERROR",
            status_code=409,
            details=details
        )

class RateLimitError(XiheException):
    """限流错误"""
    
    def __init__(self, message: str = "请求过于频繁", details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=message,
            error_code="RATE_LIMIT_EXCEEDED",
            status_code=429,
            details=details
        )

class AIProviderError(XiheException):
    """AI提供商错误"""
    
    def __init__(self, message: str, provider: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"[{provider}] {message}",
            error_code="AI_PROVIDER_ERROR",
            status_code=502,
            details=details
        )

class TaskExecutionError(XiheException):
    """任务执行错误"""
    
    def __init__(self, message: str, task_id: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"任务执行失败: {message}",
            error_code="TASK_EXECUTION_ERROR",
            status_code=500,
            details={"task_id": task_id, **(details or {})}
        )

class DesktopAutomationError(XiheException):
    """桌面自动化错误"""
    
    def __init__(self, message: str, action: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"桌面操作失败: {message}",
            error_code="DESKTOP_AUTOMATION_ERROR",
            status_code=500,
            details={"action": action, **(details or {})}
        )

class FileProcessingError(XiheException):
    """文件处理错误"""
    
    def __init__(self, message: str, filename: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"文件处理失败: {message}",
            error_code="FILE_PROCESSING_ERROR",
            status_code=500,
            details={"filename": filename, **(details or {})}
        )

class DatabaseError(XiheException):
    """数据库错误"""
    
    def __init__(self, message: str, operation: str, details: Optional[Dict[str, Any]] = None):
        super().__init__(
            message=f"数据库操作失败: {message}",
            error_code="DATABASE_ERROR",
            status_code=500,
            details={"operation": operation, **(details or {})}
        )