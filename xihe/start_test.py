#!/usr/bin/env python3
"""
羲和项目启动测试脚本
测试项目是否能正常启动（不依赖外部包）
"""

import sys
import os
import asyncio
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

def test_config_loading():
    """测试配置加载"""
    print("🔧 测试配置加载...")
    
    try:
        # 设置环境变量
        os.environ["SECRET_KEY"] = "test-secret-key-for-testing"
        os.environ["DATABASE_URL"] = "sqlite:///test.db"
        os.environ["ENCRYPTION_KEY"] = "test-encryption-key"
        
        from core.config import Settings
        
        # 创建配置实例
        settings = Settings(
            SECRET_KEY="test-secret-key",
            DATABASE_URL="sqlite:///test.db",
            ENCRYPTION_KEY="test-encryption-key"
        )
        
        print(f"✅ 配置加载成功: {settings.APP_NAME} v{settings.VERSION}")
        return True
        
    except Exception as e:
        print(f"❌ 配置加载失败: {e}")
        return False

def test_database_models():
    """测试数据库模型"""
    print("\n📊 测试数据库模型...")
    
    try:
        from models.user import User, UserProfile, UserSettings
        from models.task import Task, TaskStep, TaskStatus, TaskPriority, TaskType
        from models.agent import Agent, AgentType, AgentStatus
        
        # 测试模型创建
        user = User(
            username="test_user",
            email="test@example.com",
            hashed_password="hashed_password"
        )
        
        task = Task(
            user_id=1,
            title="测试任务",
            description="这是一个测试任务",
            task_type=TaskType.DESKTOP_AUTOMATION,
            priority=TaskPriority.NORMAL
        )
        
        agent = Agent(
            name="测试代理",
            agent_type=AgentType.PLANNER,
            status=AgentStatus.IDLE
        )
        
        print("✅ 数据库模型创建成功")
        return True
        
    except Exception as e:
        print(f"❌ 数据库模型测试失败: {e}")
        return False

async def test_ai_system():
    """测试AI系统"""
    print("\n🤖 测试AI系统...")
    
    try:
        from core.ai_providers import MockAIProvider, AIProviderType, AIProviderManager
        
        # 测试AI提供商
        provider = MockAIProvider(AIProviderType.OPENAI, "gpt-4")
        await provider.initialize()
        
        # 测试生成响应
        messages = [{"role": "user", "content": "Hello, how are you?"}]
        response = await provider.generate_response(messages)
        
        print(f"✅ AI系统测试成功: {response[:50]}...")
        
        # 测试提供商管理器
        manager = AIProviderManager()
        await manager.initialize()
        providers = await manager.get_available_providers()
        
        print(f"✅ 可用AI提供商: {len(providers)} 个")
        return True
        
    except Exception as e:
        print(f"❌ AI系统测试失败: {e}")
        return False

async def test_agent_system():
    """测试代理系统"""
    print("\n🎯 测试代理系统...")
    
    try:
        from agents.core.agent import BaseAgent, AgentType, AgentStatus, AgentContext, AgentMessage
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
        
        # 测试代理状态
        print(f"✅ 代理创建成功: {agent.name}")
        print(f"✅ 代理状态: {agent.status.value}")
        
        return True
        
    except Exception as e:
        print(f"❌ 代理系统测试失败: {e}")
        return False

def test_api_structure():
    """测试API结构"""
    print("\n🌐 测试API结构...")
    
    try:
        from api.v1.auth import router as auth_router
        from api.v1.users import router as users_router
        from api.v1.tasks import router as tasks_router
        
        print("✅ API路由导入成功")
        
        # 检查路由是否有端点
        auth_routes = [route.path for route in auth_router.routes]
        users_routes = [route.path for route in users_router.routes]
        tasks_routes = [route.path for route in tasks_router.routes]
        
        print(f"✅ 认证路由: {len(auth_routes)} 个端点")
        print(f"✅ 用户路由: {len(users_routes)} 个端点")
        print(f"✅ 任务路由: {len(tasks_routes)} 个端点")
        
        return True
        
    except Exception as e:
        print(f"❌ API结构测试失败: {e}")
        return False

def test_services():
    """测试服务层"""
    print("\n⚙️ 测试服务层...")
    
    try:
        from services.auth_service import AuthService
        from services.user_service import UserService
        from services.task_service import TaskService
        
        # 测试认证服务
        auth_service = AuthService()
        test_password = "test123456"
        hashed = auth_service.get_password_hash(test_password)
        verified = auth_service.verify_password(test_password, hashed)
        
        if not verified:
            print("❌ 密码哈希验证失败")
            return False
        
        print("✅ 认证服务测试通过")
        
        # 测试其他服务
        user_service = UserService()
        task_service = TaskService()
        
        print("✅ 服务层初始化成功")
        return True
        
    except Exception as e:
        print(f"❌ 服务层测试失败: {e}")
        return False

def test_main_app():
    """测试主应用"""
    print("\n🚀 测试主应用...")
    
    try:
        # 检查main.py是否可以导入
        import main
        
        print("✅ 主应用模块导入成功")
        
        # 检查FastAPI应用是否创建
        if hasattr(main, 'app'):
            print("✅ FastAPI应用创建成功")
            return True
        else:
            print("❌ FastAPI应用未创建")
            return False
        
    except Exception as e:
        print(f"❌ 主应用测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始羲和项目启动测试...\n")
    
    tests = [
        ("配置加载", test_config_loading),
        ("数据库模型", test_database_models),
        ("AI系统", test_ai_system),
        ("代理系统", test_agent_system),
        ("API结构", test_api_structure),
        ("服务层", test_services),
        ("主应用", test_main_app)
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
        print("\n🎉 所有测试通过！")
        print("✅ 羲和项目可以正常启动和运行")
        print("\n📝 运行说明:")
        print("1. 安装依赖: pip install -r backend/requirements.txt")
        print("2. 启动后端: cd backend && python main.py")
        print("3. 启动前端: cd frontend && npm install && npm start")
        print("4. 访问应用: http://localhost:8000")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查相关模块")
        print("💡 提示: 某些功能需要安装依赖包才能完全测试")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)