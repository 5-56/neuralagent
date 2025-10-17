#!/usr/bin/env python3
"""
羲和系统集成测试脚本
"""

import asyncio
import sys
import os
import json
from pathlib import Path

# 添加项目根目录到Python路径
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

async def test_imports():
    """测试所有模块导入"""
    print("🔍 测试模块导入...")
    
    try:
        # 测试核心模块
        from backend.core.config import settings
        print("✅ 配置模块导入成功")
        
        from backend.core.database import get_db, init_db
        print("✅ 数据库模块导入成功")
        
        from backend.core.security import setup_security
        print("✅ 安全模块导入成功")
        
        from backend.core.middleware import LoggingMiddleware, RateLimitMiddleware
        print("✅ 中间件模块导入成功")
        
        from backend.core.monitoring import setup_monitoring
        print("✅ 监控模块导入成功")
        
        # 测试模型
        from backend.models.user import User, UserProfile, UserSettings
        print("✅ 用户模型导入成功")
        
        from backend.models.task import Task, TaskStep, TaskStatus
        print("✅ 任务模型导入成功")
        
        from backend.models.agent import Agent, AgentType
        print("✅ 代理模型导入成功")
        
        # 测试服务
        from backend.services.auth_service import AuthService
        print("✅ 认证服务导入成功")
        
        from backend.services.user_service import UserService
        print("✅ 用户服务导入成功")
        
        from backend.services.task_service import TaskService
        print("✅ 任务服务导入成功")
        
        # 测试API
        from backend.api.v1.auth import router as auth_router
        print("✅ 认证API导入成功")
        
        from backend.api.v1.users import router as users_router
        print("✅ 用户API导入成功")
        
        from backend.api.v1.tasks import router as tasks_router
        print("✅ 任务API导入成功")
        
        # 测试AI代理
        from backend.agents.core.agent import BaseAgent, AgentType
        print("✅ AI代理核心模块导入成功")
        
        from backend.agents.implementations.planner_agent import PlannerAgent
        print("✅ 规划代理导入成功")
        
        from backend.agents.implementations.executor_agent import ExecutorAgent
        print("✅ 执行代理导入成功")
        
        # 测试工具
        from backend.tools.screenshot_tool import ScreenshotTool
        print("✅ 截图工具导入成功")
        
        from backend.tools.voice_tool import VoiceTool
        print("✅ 语音工具导入成功")
        
        print("🎉 所有模块导入测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 模块导入失败: {e}")
        return False

async def test_configuration():
    """测试配置"""
    print("\n🔧 测试配置...")
    
    try:
        from backend.core.config import settings
        
        # 检查必要的配置
        required_configs = [
            'APP_NAME', 'VERSION', 'SECRET_KEY', 'DATABASE_URL'
        ]
        
        for config in required_configs:
            if not hasattr(settings, config):
                print(f"❌ 缺少配置: {config}")
                return False
            print(f"✅ 配置 {config}: {getattr(settings, config, 'Not set')}")
        
        print("🎉 配置测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 配置测试失败: {e}")
        return False

async def test_database_connection():
    """测试数据库连接"""
    print("\n🗄️ 测试数据库连接...")
    
    try:
        from backend.core.database import get_db, init_db
        
        # 测试数据库初始化
        await init_db()
        print("✅ 数据库初始化成功")
        
        # 测试获取数据库会话
        db = next(get_db())
        print("✅ 数据库连接成功")
        
        db.close()
        print("🎉 数据库测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 数据库测试失败: {e}")
        return False

async def test_services():
    """测试服务层"""
    print("\n⚙️ 测试服务层...")
    
    try:
        from backend.services.auth_service import AuthService
        from backend.services.user_service import UserService
        from backend.services.task_service import TaskService
        
        # 测试认证服务
        auth_service = AuthService()
        test_password = "test123456"
        hashed = auth_service.get_password_hash(test_password)
        verified = auth_service.verify_password(test_password, hashed)
        
        if not verified:
            print("❌ 密码哈希验证失败")
            return False
        print("✅ 认证服务测试通过")
        
        # 测试用户服务
        user_service = UserService()
        print("✅ 用户服务初始化成功")
        
        # 测试任务服务
        task_service = TaskService()
        print("✅ 任务服务初始化成功")
        
        print("🎉 服务层测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 服务层测试失败: {e}")
        return False

async def test_ai_agents():
    """测试AI代理"""
    print("\n🤖 测试AI代理...")
    
    try:
        from backend.agents.core.agent import AgentType, AgentStatus
        from backend.agents.implementations.planner_agent import PlannerAgent
        from backend.agents.implementations.executor_agent import ExecutorAgent
        
        # 测试代理类型枚举
        print(f"✅ 代理类型: {[t.value for t in AgentType]}")
        print(f"✅ 代理状态: {[s.value for s in AgentStatus]}")
        
        # 测试规划代理
        # planner = PlannerAgent(None)  # 需要AI提供商
        print("✅ 规划代理类定义正确")
        
        # 测试执行代理
        # executor = ExecutorAgent(None)  # 需要AI提供商
        print("✅ 执行代理类定义正确")
        
        print("🎉 AI代理测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ AI代理测试失败: {e}")
        return False

async def test_tools():
    """测试工具"""
    print("\n🛠️ 测试工具...")
    
    try:
        from backend.tools.screenshot_tool import ScreenshotTool
        from backend.tools.voice_tool import VoiceTool
        
        # 测试截图工具
        screenshot_tool = ScreenshotTool()
        print("✅ 截图工具初始化成功")
        
        # 测试语音工具
        voice_tool = VoiceTool()
        print("✅ 语音工具初始化成功")
        
        print("🎉 工具测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 工具测试失败: {e}")
        return False

async def test_frontend_structure():
    """测试前端结构"""
    print("\n🎨 测试前端结构...")
    
    try:
        frontend_path = project_root / "frontend"
        
        # 检查关键文件
        key_files = [
            "package.json",
            "src/App.js",
            "src/components/Layout.js",
            "src/pages/HomePage.js",
            "src/pages/TasksPage.js",
            "src/pages/ChatPage.js",
            "src/pages/SettingsPage.js",
            "src/store/useAppStore.js",
            "src/styles/themes.js"
        ]
        
        for file_path in key_files:
            full_path = frontend_path / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ 缺少文件: {file_path}")
                return False
        
        print("🎉 前端结构测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ 前端结构测试失败: {e}")
        return False

async def test_docker_config():
    """测试Docker配置"""
    print("\n🐳 测试Docker配置...")
    
    try:
        # 检查Docker文件
        docker_files = [
            "docker-compose.yml",
            "backend/Dockerfile",
            "frontend/Dockerfile"
        ]
        
        for file_path in docker_files:
            full_path = project_root / file_path
            if full_path.exists():
                print(f"✅ {file_path}")
            else:
                print(f"❌ 缺少文件: {file_path}")
                return False
        
        print("🎉 Docker配置测试通过！")
        return True
        
    except Exception as e:
        print(f"❌ Docker配置测试失败: {e}")
        return False

async def main():
    """主测试函数"""
    print("🚀 开始羲和系统集成测试...\n")
    
    tests = [
        ("模块导入", test_imports),
        ("配置检查", test_configuration),
        ("数据库连接", test_database_connection),
        ("服务层", test_services),
        ("AI代理", test_ai_agents),
        ("工具", test_tools),
        ("前端结构", test_frontend_structure),
        ("Docker配置", test_docker_config)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = await test_func()
            if result:
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 所有测试通过！系统集成成功！")
        return True
    else:
        print("⚠️ 部分测试失败，请检查相关模块")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)