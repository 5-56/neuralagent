"""
AI提供商管理模块
支持多种AI服务提供商
"""

import asyncio
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Union
from enum import Enum
import logging

from langchain_openai import ChatOpenAI, AzureChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_aws import ChatBedrockConverse
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import BaseMessage

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
        messages: List[BaseMessage], 
        **kwargs
    ) -> str:
        """生成响应"""
        pass
    
    @abstractmethod
    async def generate_streaming_response(
        self, 
        messages: List[BaseMessage], 
        **kwargs
    ) -> Any:
        """生成流式响应"""
        pass
    
    @abstractmethod
    async def health_check(self) -> bool:
        """健康检查"""
        pass


class OpenAIProvider(AIProvider):
    """OpenAI提供商"""
    
    def __init__(self, model: str = None, **kwargs):
        super().__init__(AIProviderType.OPENAI, model or settings.OPENAI_MODEL, **kwargs)
    
    async def initialize(self) -> None:
        """初始化OpenAI客户端"""
        if not settings.OPENAI_API_KEY:
            raise AIProviderError("OpenAI API密钥未配置", "openai")
        
        self._client = ChatOpenAI(
            model=self.model,
            api_key=settings.OPENAI_API_KEY,
            base_url=settings.OPENAI_BASE_URL,
            **self.kwargs
        )
        logger.info(f"OpenAI提供商初始化完成，模型: {self.model}")
    
    async def generate_response(self, messages: List[BaseMessage], **kwargs) -> str:
        """生成响应"""
        if not self._client:
            await self.initialize()
        
        try:
            response = await self._client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            raise AIProviderError(f"生成响应失败: {str(e)}", "openai")
    
    async def generate_streaming_response(self, messages: List[BaseMessage], **kwargs):
        """生成流式响应"""
        if not self._client:
            await self.initialize()
        
        try:
            async for chunk in self._client.astream(messages, **kwargs):
                yield chunk
        except Exception as e:
            raise AIProviderError(f"生成流式响应失败: {str(e)}", "openai")
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                await self.initialize()
            
            # 发送简单测试请求
            test_messages = [{"role": "user", "content": "Hello"}]
            await self.generate_response(test_messages)
            return True
        except Exception as e:
            logger.error(f"OpenAI健康检查失败: {e}")
            return False


class AnthropicProvider(AIProvider):
    """Anthropic提供商"""
    
    def __init__(self, model: str = None, **kwargs):
        super().__init__(AIProviderType.ANTHROPIC, model or settings.ANTHROPIC_MODEL, **kwargs)
    
    async def initialize(self) -> None:
        """初始化Anthropic客户端"""
        if not settings.ANTHROPIC_API_KEY:
            raise AIProviderError("Anthropic API密钥未配置", "anthropic")
        
        self._client = ChatAnthropic(
            model=self.model,
            api_key=settings.ANTHROPIC_API_KEY,
            **self.kwargs
        )
        logger.info(f"Anthropic提供商初始化完成，模型: {self.model}")
    
    async def generate_response(self, messages: List[BaseMessage], **kwargs) -> str:
        """生成响应"""
        if not self._client:
            await self.initialize()
        
        try:
            response = await self._client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            raise AIProviderError(f"生成响应失败: {str(e)}", "anthropic")
    
    async def generate_streaming_response(self, messages: List[BaseMessage], **kwargs):
        """生成流式响应"""
        if not self._client:
            await self.initialize()
        
        try:
            async for chunk in self._client.astream(messages, **kwargs):
                yield chunk
        except Exception as e:
            raise AIProviderError(f"生成流式响应失败: {str(e)}", "anthropic")
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                await self.initialize()
            
            test_messages = [{"role": "user", "content": "Hello"}]
            await self.generate_response(test_messages)
            return True
        except Exception as e:
            logger.error(f"Anthropic健康检查失败: {e}")
            return False


class GoogleProvider(AIProvider):
    """Google Gemini提供商"""
    
    def __init__(self, model: str = None, **kwargs):
        super().__init__(AIProviderType.GOOGLE, model or settings.GOOGLE_MODEL, **kwargs)
    
    async def initialize(self) -> None:
        """初始化Google客户端"""
        if not settings.GOOGLE_API_KEY:
            raise AIProviderError("Google API密钥未配置", "google")
        
        self._client = ChatGoogleGenerativeAI(
            model=self.model,
            google_api_key=settings.GOOGLE_API_KEY,
            **self.kwargs
        )
        logger.info(f"Google提供商初始化完成，模型: {self.model}")
    
    async def generate_response(self, messages: List[BaseMessage], **kwargs) -> str:
        """生成响应"""
        if not self._client:
            await self.initialize()
        
        try:
            response = await self._client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            raise AIProviderError(f"生成响应失败: {str(e)}", "google")
    
    async def generate_streaming_response(self, messages: List[BaseMessage], **kwargs):
        """生成流式响应"""
        if not self._client:
            await self.initialize()
        
        try:
            async for chunk in self._client.astream(messages, **kwargs):
                yield chunk
        except Exception as e:
            raise AIProviderError(f"生成流式响应失败: {str(e)}", "google")
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                await self.initialize()
            
            test_messages = [{"role": "user", "content": "Hello"}]
            await self.generate_response(test_messages)
            return True
        except Exception as e:
            logger.error(f"Google健康检查失败: {e}")
            return False


class OllamaProvider(AIProvider):
    """Ollama本地模型提供商"""
    
    def __init__(self, model: str = None, **kwargs):
        super().__init__(AIProviderType.OLLAMA, model or settings.OLLAMA_MODEL, **kwargs)
    
    async def initialize(self) -> None:
        """初始化Ollama客户端"""
        self._client = ChatOllama(
            model=self.model,
            base_url=settings.OLLAMA_BASE_URL,
            **self.kwargs
        )
        logger.info(f"Ollama提供商初始化完成，模型: {self.model}")
    
    async def generate_response(self, messages: List[BaseMessage], **kwargs) -> str:
        """生成响应"""
        if not self._client:
            await self.initialize()
        
        try:
            response = await self._client.ainvoke(messages, **kwargs)
            return response.content
        except Exception as e:
            raise AIProviderError(f"生成响应失败: {str(e)}", "ollama")
    
    async def generate_streaming_response(self, messages: List[BaseMessage], **kwargs):
        """生成流式响应"""
        if not self._client:
            await self.initialize()
        
        try:
            async for chunk in self._client.astream(messages, **kwargs):
                yield chunk
        except Exception as e:
            raise AIProviderError(f"生成流式响应失败: {str(e)}", "ollama")
    
    async def health_check(self) -> bool:
        """健康检查"""
        try:
            if not self._client:
                await self.initialize()
            
            test_messages = [{"role": "user", "content": "Hello"}]
            await self.generate_response(test_messages)
            return True
        except Exception as e:
            logger.error(f"Ollama健康检查失败: {e}")
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
        
        # 根据配置初始化提供商
        providers_to_init = []
        
        if settings.OPENAI_API_KEY:
            providers_to_init.append(OpenAIProvider())
        
        if settings.ANTHROPIC_API_KEY:
            providers_to_init.append(AnthropicProvider())
        
        if settings.GOOGLE_API_KEY:
            providers_to_init.append(GoogleProvider())
        
        # Ollama总是尝试初始化（本地服务）
        providers_to_init.append(OllamaProvider())
        
        # 初始化提供商
        for provider in providers_to_init:
            try:
                await provider.initialize()
                self._providers[provider.provider_type] = provider
                logger.info(f"提供商 {provider.provider_type} 初始化成功")
            except Exception as e:
                logger.warning(f"提供商 {provider.provider_type} 初始化失败: {e}")
        
        self._initialized = True
        logger.info(f"AI提供商管理器初始化完成，可用提供商: {list(self._providers.keys())}")
    
    async def get_provider(self, provider_type: AIProviderType) -> AIProvider:
        """获取指定类型的提供商"""
        if not self._initialized:
            await self.initialize()
        
        if provider_type not in self._providers:
            raise AIProviderError(f"提供商 {provider_type} 不可用", provider_type.value)
        
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