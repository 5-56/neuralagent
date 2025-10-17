"""
AI提供商管理模块
支持多种AI服务提供商
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import logging

from core.config import settings
from core.exceptions import AIProviderError

logger = logging.getLogger(__name__)


class AIProviderType(str, Enum):
    """AI提供商类型"""
    OPENAI = "openai"
    ANTHROPIC = "anthropic"
    GOOGLE = "google"
    AZURE_OPENAI = "azure_openai"
    BEDROCK = "bedrock"
    OLLAMA = "ollama"
    LOCAL = "local"


class AIProvider(ABC):
    """AI提供商基类"""
    
    def __init__(self, provider_type: AIProviderType, model: str, **kwargs):
        self.provider_type = provider_type
        self.model = model
        self.kwargs = kwargs
        self._client = None
    
    @abstractmethod
    async def initialize(self) -> None:
        """初始化提供商客户端"""
        pass
    
    @abstractmethod
    async def generate_response(
        self, 
        messages: List[dict], 
        **kwargs
    ) -> str:
        """生成响应"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
        pass


class MockAIProvider(AIProvider):
    """模拟AI提供商（用于测试）"""
    
    def __init__(self, provider_type: AIProviderType, model: str = "mock-model", **kwargs):
        super().__init__(provider_type, model, **kwargs)
    
    async def initialize(self) -> None:
        """初始化模拟客户端"""
        self._client = "mock_client"
        logger.info(f"模拟AI提供商初始化完成，类型: {self.provider_type}")
    
    async def generate_response(self, messages: List[dict], **kwargs) -> str:
        """生成模拟响应"""
        if not self._client:
            await self.initialize()
        
        # 模拟AI响应
        last_message = messages[-1] if messages else {"content": "Hello"}
        content = last_message.get("content", "Hello")
        
        if "任务" in content or "task" in content.lower():
            return "我理解您想要创建一个任务。让我为您分析并制定执行计划..."
        elif "帮助" in content or "help" in content.lower():
            return "我是羲和AI助手，可以帮助您进行桌面自动化、任务管理和智能对话。"
        else:
            return f"我收到了您的消息：{content}。作为AI助手，我随时为您服务。"
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                await self.initialize()
            return True
        except Exception as e:
            logger.error(f"模拟AI提供商健康检查失败: {e}")
            return False


class AIProviderManager:
    """AI提供商管理器"""
    
    def __init__(self):
        self._providers: Dict[AIProviderType, AIProvider] = {}
        self._initialized = False
    
    async def initialize(self) -> None:
        """初始化所有可用的提供商"""
        if self._initialized:
            return
        
        # 创建模拟提供商
        mock_providers = [
            MockAIProvider(AIProviderType.OPENAI, "gpt-4"),
            MockAIProvider(AIProviderType.ANTHROPIC, "claude-3"),
            MockAIProvider(AIProviderType.GOOGLE, "gemini-pro"),
            MockAIProvider(AIProviderType.OLLAMA, "llama2")
        ]
        
        # 初始化提供商
        for provider in mock_providers:
            try:
                await provider.initialize()
                self._providers[provider.provider_type] = provider
                logger.info(f"提供商 {provider.provider_type} 初始化成功")
            except Exception as e:
                logger.warning(f"提供商 {provider.provider_type} 初始化失败: {e}")
        
        self._initialized = True
        logger.info(f"AI提供商管理器初始化完成，可用提供商: {list(self._providers.keys())}")
    
    async def get_provider(self, provider_type: Union[AIProviderType, str]) -> AIProvider:
        """获取指定类型的提供商"""
        if not self._initialized:
            await self.initialize()
        
        if isinstance(provider_type, str):
            try:
                provider_type = AIProviderType(provider_type)
            except ValueError:
                raise AIProviderError(f"无效的提供商类型: {provider_type}", provider_type)
        
        if provider_type not in self._providers:
            # 返回默认提供商
            if AIProviderType.OPENAI in self._providers:
                return self._providers[AIProviderType.OPENAI]
            elif self._providers:
                return list(self._providers.values())[0]
            else:
                raise AIProviderError(f"没有可用的AI提供商", provider_type.value)
        
        return self._providers[provider_type]
    
    async def get_available_providers(self) -> List[AIProviderType]:
        """获取可用的提供商列表"""
        if not self._initialized:
            await self.initialize()
        
        return list(self._providers.keys())
    
    async def health_check_all(self) -> Dict[AIProviderType, bool]:
        """检查所有提供商健康状态"""
        if not self._initialized:
            await self.initialize()
        
        results = {}
        for provider_type, provider in self._providers.items():
            try:
                results[provider_type] = await provider.health_check()
            except Exception as e:
                logger.error(f"提供商 {provider_type} 健康检查失败: {e}")
                results[provider_type] = False
        
        return results


# 全局提供商管理器实例
provider_manager = AIProviderManager()