# 监控系统实现
import logging
import time
from typing import Dict, Any
from prometheus_client import Counter, Histogram, Gauge, start_http_server, CollectorRegistry
from core.config import settings

logger = logging.getLogger(__name__)

# 创建Prometheus指标
registry = CollectorRegistry()

# HTTP请求指标
http_requests_total = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code'],
    registry=registry
)

http_request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint'],
    registry=registry
)

# 业务指标
tasks_created_total = Counter(
    'tasks_created_total',
    'Total tasks created',
    ['task_type'],
    registry=registry
)

tasks_completed_total = Counter(
    'tasks_completed_total',
    'Total tasks completed',
    ['task_type', 'status'],
    registry=registry
)

active_agents = Gauge(
    'active_agents',
    'Number of active AI agents',
    ['agent_type'],
    registry=registry
)

ai_requests_total = Counter(
    'ai_requests_total',
    'Total AI requests',
    ['provider', 'model'],
    registry=registry
)

ai_request_duration = Histogram(
    'ai_request_duration_seconds',
    'AI request duration in seconds',
    ['provider', 'model'],
    registry=registry
)

# 系统指标
system_memory_usage = Gauge(
    'system_memory_usage_bytes',
    'System memory usage in bytes',
    registry=registry
)

system_cpu_usage = Gauge(
    'system_cpu_usage_percent',
    'System CPU usage percentage',
    registry=registry
)

database_connections = Gauge(
    'database_connections_active',
    'Active database connections',
    registry=registry
)

def setup_monitoring():
    """设置监控系统"""
    if not settings.ENABLE_METRICS:
        logger.info("监控系统已禁用")
        return
    
    try:
        # 启动Prometheus指标服务器
        start_http_server(settings.METRICS_PORT, registry=registry)
        logger.info(f"监控系统已启动，指标端口: {settings.METRICS_PORT}")
        
        # 启动系统指标收集
        start_system_metrics_collection()
        
    except Exception as e:
        logger.error(f"监控系统启动失败: {e}")

def start_system_metrics_collection():
    """启动系统指标收集"""
    import threading
    import psutil
    
    def collect_system_metrics():
        while True:
            try:
                # 收集内存使用情况
                memory = psutil.virtual_memory()
                system_memory_usage.set(memory.used)
                
                # 收集CPU使用情况
                cpu_percent = psutil.cpu_percent(interval=1)
                system_cpu_usage.set(cpu_percent)
                
                # 收集数据库连接数（模拟）
                database_connections.set(5)  # 这里应该从实际的数据库连接池获取
                
                time.sleep(30)  # 每30秒收集一次
                
            except Exception as e:
                logger.error(f"系统指标收集失败: {e}")
                time.sleep(60)  # 出错时等待更长时间
    
    # 在后台线程中运行
    metrics_thread = threading.Thread(target=collect_system_metrics, daemon=True)
    metrics_thread.start()
    logger.info("系统指标收集已启动")

def record_http_request(method: str, endpoint: str, status_code: int, duration: float):
    """记录HTTP请求指标"""
    http_requests_total.labels(
        method=method,
        endpoint=endpoint,
        status_code=status_code
    ).inc()
    
    http_request_duration.labels(
        method=method,
        endpoint=endpoint
    ).observe(duration)

def record_task_created(task_type: str):
    """记录任务创建指标"""
    tasks_created_total.labels(task_type=task_type).inc()

def record_task_completed(task_type: str, status: str):
    """记录任务完成指标"""
    tasks_completed_total.labels(
        task_type=task_type,
        status=status
    ).inc()

def record_agent_status(agent_type: str, active: bool):
    """记录代理状态指标"""
    if active:
        active_agents.labels(agent_type=agent_type).inc()
    else:
        active_agents.labels(agent_type=agent_type).dec()

def record_ai_request(provider: str, model: str, duration: float):
    """记录AI请求指标"""
    ai_requests_total.labels(
        provider=provider,
        model=model
    ).inc()
    
    ai_request_duration.labels(
        provider=provider,
        model=model
    ).observe(duration)

class MetricsCollector:
    """指标收集器"""
    
    def __init__(self):
        self.start_time = time.time()
    
    def get_health_status(self) -> Dict[str, Any]:
        """获取健康状态"""
        uptime = time.time() - self.start_time
        
        return {
            "status": "healthy",
            "uptime_seconds": uptime,
            "uptime_human": self._format_uptime(uptime),
            "metrics_enabled": settings.ENABLE_METRICS,
            "metrics_port": settings.METRICS_PORT
        }
    
    def _format_uptime(self, seconds: float) -> str:
        """格式化运行时间"""
        days = int(seconds // 86400)
        hours = int((seconds % 86400) // 3600)
        minutes = int((seconds % 3600) // 60)
        seconds = int(seconds % 60)
        
        if days > 0:
            return f"{days}天 {hours}小时 {minutes}分钟"
        elif hours > 0:
            return f"{hours}小时 {minutes}分钟"
        elif minutes > 0:
            return f"{minutes}分钟 {seconds}秒"
        else:
            return f"{seconds}秒"

# 创建全局指标收集器实例
metrics_collector = MetricsCollector()