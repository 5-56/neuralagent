"""
AI代理核心模块
定义智能代理的基础架构和通用功能
"""

import asyncio
import logging
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from enum import Enum
from dataclasses import dataclass
from datetime import datetime

from core.ai_providers import AIProvider, AIProviderType, provider_manager
from core.desktop_automation import DesktopAutomation, ActionType
from core.exceptions import AIProviderError, DesktopAutomationError

logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    """代理类型枚举"""
    PLANNER = "planner"           # 任务规划代理
    EXECUTOR = "executor"         # 任务执行代理
    ANALYZER = "analyzer"         # 环境分析代理
    COORDINATOR = "coordinator"   # 协调代理
    MONITOR = "monitor"           # 监控代理


class AgentStatus(str, Enum):
    """代理状态枚举"""
    IDLE = "idle"
    THINKING = "thinking"
    EXECUTING = "executing"
    WAITING = "waiting"
    ERROR = "error"
    COMPLETED = "completed"


@dataclass
class AgentContext:
    """代理上下文"""
    task_id: str
    user_id: str
    session_id: str
    environment: Dict[str, Any]
    memory: Dict[str, Any]
    preferences: Dict[str, Any]
    created_at: datetime
    updated_at: datetime


@dataclass
class AgentMessage:
    """代理消息"""
    content: str
    message_type: str  # text, image, audio, action
    metadata: Dict[str, Any]
    timestamp: datetime
    sender: str
    recipient: str


class BaseAgent(ABC):
    """AI代理基类"""
    
    def __init__(
        self,
        agent_type: AgentType,
        provider_type: AIProviderType,
        model: Optional[str] = None,
        **kwargs
    ):
        self.agent_type = agent_type
        self.provider_type = provider_type
        self.model = model
        self.kwargs = kwargs
        self.status = AgentStatus.IDLE
        self.context: Optional[AgentContext] = None
        self.provider: Optional[AIProvider] = None
        self.desktop_automation = DesktopAutomation()
        self._message_history: List[AgentMessage] = []
        
        logger.info(f"代理 {agent_type} 初始化完成，提供商: {provider_type}")
    
    async def initialize(self) -> None:
        """初始化代理"""
        try:
            # 获取AI提供商
            self.provider = await provider_manager.get_provider(self.provider_type)
            logger.info(f"代理 {self.agent_type} 初始化完成")
        except Exception as e:
            logger.error(f"代理 {self.agent_type} 初始化失败: {e}")
            raise
    
    async def set_context(self, context: AgentContext) -> None:
        """设置代理上下文"""
        self.context = context
        logger.info(f"代理 {self.agent_type} 上下文已设置")
    
    async def process_message(self, message: AgentMessage) -> AgentMessage:
        """处理消息"""
        if not self.provider:
            await self.initialize()
        
        self.status = AgentStatus.THINKING
        self._message_history.append(message)
        
        try:
            # 生成响应
            response = await self._generate_response(message)
            
            # 创建响应消息
            response_message = AgentMessage(
                content=response,
                message_type="text",
                metadata={"agent_type": self.agent_type.value},
                timestamp=datetime.now(),
                sender=self.agent_type.value,
                recipient=message.sender
            )
            
            self._message_history.append(response_message)
            self.status = AgentStatus.IDLE
            
            return response_message
        
        except Exception as e:
            logger.error(f"代理 {self.agent_type} 处理消息失败: {e}")
            self.status = AgentStatus.ERROR
            
            error_message = AgentMessage(
                content=f"处理消息时发生错误: {str(e)}",
                message_type="error",
                metadata={"error": str(e)},
                timestamp=datetime.now(),
                sender=self.agent_type.value,
                recipient=message.sender
            )
            
            return error_message
    
    @abstractmethod
    async def _generate_response(self, message: AgentMessage) -> str:
        """生成响应（子类实现）"""
        pass
    
    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """执行桌面操作"""
        try:
            self.status = AgentStatus.EXECUTING
            result = await self.desktop_automation.execute_action(action)
            self.status = AgentStatus.IDLE
            return result
        except Exception as e:
            logger.error(f"代理 {self.agent_type} 执行操作失败: {e}")
            self.status = AgentStatus.ERROR
            raise DesktopAutomationError(f"执行操作失败: {str(e)}", action.get("type", "unknown"))
    
    async def get_environment_info(self) -> Dict[str, Any]:
        """获取环境信息"""
        return {
            "screen_info": self.desktop_automation.get_screen_info(),
            "running_apps": self.desktop_automation.get_running_apps(),
            "timestamp": datetime.now().isoformat()
        }
    
    def get_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        return {
            "agent_type": self.agent_type.value,
            "status": self.status.value,
            "provider": self.provider_type.value,
            "model": self.model,
            "message_count": len(self._message_history),
            "context_available": self.context is not None
        }


class PlannerAgent(BaseAgent):
    """任务规划代理"""
    
    def __init__(self, **kwargs):
        super().__init__(AgentType.PLANNER, AIProviderType.OPENAI, **kwargs)
    
    async def _generate_response(self, message: AgentMessage) -> str:
        """生成任务规划响应"""
        # 构建规划提示
        prompt = self._build_planning_prompt(message)
        
        # 调用AI提供商生成响应
        response = await self.provider.generate_response(prompt)
        
        return response
    
    def _build_planning_prompt(self, message: AgentMessage) -> List[Dict[str, str]]:
        """构建规划提示"""
        return [
            {
                "role": "system",
                "content": """你是一个智能任务规划代理。你的职责是：
1. 分析用户的任务需求
2. 将复杂任务分解为可执行的子任务
3. 为每个子任务制定详细的执行计划
4. 考虑任务之间的依赖关系
5. 提供风险评估和备选方案

请以JSON格式返回规划结果，包含：
- task_analysis: 任务分析
- subtasks: 子任务列表
- execution_plan: 执行计划
- dependencies: 依赖关系
- risks: 风险评估
- alternatives: 备选方案"""
            },
            {
                "role": "user",
                "content": f"请为以下任务制定执行计划：\n\n{message.content}"
            }
        ]


class ExecutorAgent(BaseAgent):
    """任务执行代理"""
    
    def __init__(self, **kwargs):
        super().__init__(AgentType.EXECUTOR, AIProviderType.ANTHROPIC, **kwargs)
    
    async def _generate_response(self, message: AgentMessage) -> str:
        """生成执行响应"""
        # 获取当前环境信息
        environment = await self.get_environment_info()
        
        # 构建执行提示
        prompt = self._build_execution_prompt(message, environment)
        
        # 调用AI提供商生成响应
        response = await self.provider.generate_response(prompt)
        
        return response
    
    def _build_execution_prompt(self, message: AgentMessage, environment: Dict[str, Any]) -> List[Dict[str, str]]:
        """构建执行提示"""
        return [
            {
                "role": "system",
                "content": """你是一个智能任务执行代理。你的职责是：
1. 理解具体的执行任务
2. 分析当前桌面环境状态
3. 生成精确的桌面操作指令
4. 确保操作的安全性和准确性
5. 提供操作反馈和状态更新

请以JSON格式返回执行结果，包含：
- action_type: 操作类型
- parameters: 操作参数
- coordinates: 坐标信息（如适用）
- text: 输入文本（如适用）
- confidence: 操作置信度
- reasoning: 操作理由"""
            },
            {
                "role": "user",
                "content": f"""请执行以下任务：

任务描述：{message.content}

当前环境：
- 屏幕分辨率：{environment['screen_info']['width']}x{environment['screen_info']['height']}
- 运行应用：{environment['running_apps'][:5]}  # 显示前5个应用

请生成具体的操作指令。"""
            }
        ]


class AnalyzerAgent(BaseAgent):
    """环境分析代理"""
    
    def __init__(self, **kwargs):
        super().__init__(AgentType.ANALYZER, AIProviderType.GOOGLE, **kwargs)
    
    async def _generate_response(self, message: AgentMessage) -> str:
        """生成分析响应"""
        # 获取环境信息
        environment = await self.get_environment_info()
        
        # 构建分析提示
        prompt = self._build_analysis_prompt(message, environment)
        
        # 调用AI提供商生成响应
        response = await self.provider.generate_response(prompt)
        
        return response
    
    def _build_analysis_prompt(self, message: AgentMessage, environment: Dict[str, Any]) -> List[Dict[str, str]]:
        """构建分析提示"""
        return [
            {
                "role": "system",
                "content": """你是一个智能环境分析代理。你的职责是：
1. 分析桌面环境的当前状态
2. 识别可交互的UI元素
3. 评估操作可行性
4. 提供环境优化建议
5. 检测潜在的安全风险

请以JSON格式返回分析结果，包含：
- environment_status: 环境状态
- interactive_elements: 可交互元素
- feasibility: 操作可行性
- recommendations: 优化建议
- risks: 安全风险"""
            },
            {
                "role": "user",
                "content": f"""请分析当前桌面环境：

分析需求：{message.content}

环境信息：
- 屏幕分辨率：{environment['screen_info']['width']}x{environment['screen_info']['height']}
- 运行应用：{environment['running_apps'][:10]}  # 显示前10个应用

请提供详细的环境分析。"""
            }
        ]


class AgentManager:
    """代理管理器"""
    
    def __init__(self):
        self._agents: Dict[AgentType, BaseAgent] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """初始化所有代理"""
        if self._initialized:
            return
        
        # 创建代理实例
        self._agents[AgentType.PLANNER] = PlannerAgent()
        self._agents[AgentType.EXECUTOR] = ExecutorAgent()
        self._agents[AgentType.ANALYZER] = AnalyzerAgent()
        
        # 初始化所有代理
        for agent in self._agents.values():
            await agent.initialize()
        
        self._initialized = True
        logger.info("代理管理器初始化完成")
    
    async def get_agent(self, agent_type: AgentType) -> BaseAgent:
        """获取指定类型的代理"""
        if not self._initialized:
            await self.initialize()
        
        if agent_type not in self._agents:
            raise ValueError(f"代理类型 {agent_type} 不存在")
        
        return self._agents[agent_type]
    
    async def get_all_agents(self) -> Dict[AgentType, BaseAgent]:
        """获取所有代理"""
        if not self._initialized:
            await self.initialize()
        
        return self._agents.copy()
    
    async def get_agent_status(self) -> Dict[str, Dict[str, Any]]:
        """获取所有代理状态"""
        if not self._initialized:
            await self.initialize()
        
        status = {}
        for agent_type, agent in self._agents.items():
            status[agent_type.value] = agent.get_status()
        
        return status


# 全局代理管理器实例
agent_manager = AgentManager()