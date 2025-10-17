#!/usr/bin/env python3
"""
羲和基础功能测试脚本
测试核心模块是否能正常导入和初始化
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

def test_basic_imports():
    """测试基础模块导入"""
    print("🔍 测试基础模块导入...")
    
    try:
        # 测试核心配置
        from core.config import Settings
        print("✅ 配置模块导入成功")
        
        # 测试异常类
        from core.exceptions import XiheException, ValidationError
        print("✅ 异常模块导入成功")
        
        # 测试AI提供商
        from core.ai_providers import AIProviderManager, MockAIProvider
        print("✅ AI提供商模块导入成功")
        
        # 测试代理
        from agents.core.agent import BaseAgent, AgentType, AgentStatus
        print("✅ 代理核心模块导入成功")
        
        # 测试桌面自动化
        from core.desktop_automation import DesktopAutomation, ActionType
        print("✅ 桌面自动化模块导入成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 基础模块导入失败: {e}")
        return False

def test_config_creation():
    """测试配置创建"""
    print("\n🔧 测试配置创建...")
    
    try:
        from core.config import Settings
        
        # 创建测试配置
        config = Settings(
            SECRET_KEY="test-secret-key",
            DATABASE_URL="sqlite:///test.db",
            ENCRYPTION_KEY="test-encryption-key"
        )
        
        print(f"✅ 配置创建成功: {config.APP_NAME}")
        return True
        
    except Exception as e:
        print(f"❌ 配置创建失败: {e}")
        return False

async def test_ai_provider():
    """测试AI提供商"""
    print("\n🤖 测试AI提供商...")
    
    try:
        from core.ai_providers import MockAIProvider, AIProviderType
        
        # 创建模拟提供商
        provider = MockAIProvider(AIProviderType.OPENAI, "gpt-4")
        await provider.initialize()
        
        # 测试生成响应
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        response = await provider.generate_response(messages)
        
        print(f"✅ AI提供商测试成功: {response[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ AI提供商测试失败: {e}")
        return False

async def test_agent_creation():
    """测试代理创建"""
    print("\n🎯 测试代理创建...")
    
    try:
        from agents.core.agent import BaseAgent, AgentType, AgentStatus
        from core.ai_providers import MockAIProvider, AIProviderType
        
        # 创建AI提供商
        ai_provider = MockAIProvider(AIProviderType.OPENAI, "gpt-4")
        await ai_provider.initialize()
        
        # 创建代理
        agent = BaseAgent(
            agent_type=AgentType.PLANNER,
            ai_provider=ai_provider,
            name="TestAgent",
            description="测试代理"
        )
        
        print(f"✅ 代理创建成功: {agent.name}")
        return True
        
    except Exception as e:
        print(f"❌ 代理创建失败: {e}")
        return False

async def test_desktop_automation():
    """测试桌面自动化"""
    print("\n🖥️ 测试桌面自动化...")
    
    try:
        from core.desktop_automation import DesktopAutomation, ActionType
        
        # 创建桌面自动化实例
        desktop = DesktopAutomation()
        
        # 获取屏幕信息
        screen_info = desktop.get_screen_info()
        print(f"✅ 屏幕信息: {screen_info['width']}x{screen_info['height']}")
        
        # 测试等待操作（不执行实际桌面操作）
        result = await desktop.execute_action({
            "type": ActionType.WAIT,
            "params": {"duration": 0.1}
        })
        
        if result["success"]:
            print("✅ 桌面自动化测试成功")
            return True
        else:
            print("❌ 桌面自动化操作失败")
            return False
        
    except Exception as e:
        print(f"❌ 桌面自动化测试失败: {e}")
        return False

def test_models():
    """测试数据模型"""
    print("\n📊 测试数据模型...")
    
    try:
        from models.user import User, UserProfile, UserSettings
        from models.task import Task, TaskStep, TaskStatus, TaskPriority, TaskType
        from models.agent import Agent, AgentType, AgentStatus
        
        # 测试用户模型
        user = User(
            username="test_user",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        print("✅ 用户模型创建成功")
        
        # 测试任务模型
        task = Task(
            user_id=1,
            title="测试任务",
            description="这是一个测试任务",
            task_type=TaskType.DESKTOP_AUTOMATION,
            priority=TaskPriority.NORMAL
        )
        print("✅ 任务模型创建成功")
        
        # 测试代理模型
        agent = Agent(
            name="测试代理",
            agent_type=AgentType.PLANNER,
            status=AgentStatus.IDLE
        )
        print("✅ 代理模型创建成功")
        
        return True
        
    except Exception as e:
        print(f"❌ 数据模型测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始羲和基础功能测试...\n")
    
    tests = [
        ("基础模块导入", test_basic_imports),
        ("配置创建", test_config_creation),
        ("AI提供商", test_ai_provider),
        ("代理创建", test_agent_creation),
        ("桌面自动化", test_desktop_automation),
        ("数据模型", test_models)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if asyncio.iscoroutinefunction(test_func):
                result = await test_func()
            else:
                result = test_func()
            
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有基础功能测试通过！")
        print("\n✅ 项目可以正常启动和运行")
        print("📝 注意: 需要安装依赖包才能完整运行")
        print("   运行: pip install -r backend/requirements.txt")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关模块")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)