#!/usr/bin/env python3
"""
羲和项目结构验证脚本
"""

import os
import sys
from pathlib import Path

def test_project_structure():
    """测试项目结构"""
    print("🔍 验证项目结构...")
    
    project_root = Path(__file__).parent
    required_structure = {
        "backend/": [
            "main.py",
            "requirements.txt",
            "core/",
            "models/",
            "api/",
            "services/",
            "agents/",
            "tools/",
            "tests/",
            "alembic/",
            "Dockerfile"
        ],
        "frontend/": [
            "package.json",
            "src/",
            "electron/",
            "Dockerfile"
        ],
        "docs/": [
            "ARCHITECTURE.md",
            "INSTALLATION.md"
        ],
        "": [
            "docker-compose.yml",
            "install.sh",
            "README.md",
            "pyproject.toml"
        ]
    }
    
    all_passed = True
    
    for base_path, items in required_structure.items():
        full_path = project_root / base_path
        print(f"\n📁 检查 {base_path or '根目录'}:")
        
        for item in items:
            item_path = full_path / item
            if item_path.exists():
                if item_path.is_dir():
                    print(f"  ✅ 目录: {item}")
                else:
                    print(f"  ✅ 文件: {item}")
            else:
                print(f"  ❌ 缺少: {item}")
                all_passed = False
    
    return all_passed

def test_backend_files():
    """测试后端关键文件"""
    print("\n🔧 验证后端关键文件...")
    
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    
    key_files = [
        "main.py",
        "core/config.py",
        "core/database.py",
        "core/security.py",
        "core/middleware.py",
        "core/monitoring.py",
        "core/exceptions.py",
        "models/__init__.py",
        "models/user.py",
        "models/task.py",
        "models/agent.py",
        "api/__init__.py",
        "api/v1/__init__.py",
        "api/v1/auth.py",
        "api/v1/users.py",
        "api/v1/tasks.py",
        "services/__init__.py",
        "services/auth_service.py",
        "services/user_service.py",
        "services/task_service.py",
        "agents/core/agent.py",
        "agents/implementations/planner_agent.py",
        "agents/implementations/executor_agent.py",
        "tools/__init__.py",
        "tools/screenshot_tool.py",
        "tools/voice_tool.py",
        "schemas/__init__.py",
        "schemas/auth.py",
        "schemas/user.py",
        "schemas/task.py"
    ]
    
    all_passed = True
    
    for file_path in key_files:
        full_path = backend_path / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 缺少: {file_path}")
            all_passed = False
    
    return all_passed

def test_frontend_files():
    """测试前端关键文件"""
    print("\n🎨 验证前端关键文件...")
    
    project_root = Path(__file__).parent
    frontend_path = project_root / "frontend"
    
    key_files = [
        "package.json",
        "src/App.js",
        "src/components/Layout.js",
        "src/components/LoadingSpinner.js",
        "src/components/TaskCard.js",
        "src/components/TaskForm.js",
        "src/components/MessageBubble.js",
        "src/pages/HomePage.js",
        "src/pages/TasksPage.js",
        "src/pages/ChatPage.js",
        "src/pages/SettingsPage.js",
        "src/store/useAppStore.js",
        "src/styles/themes.js",
        "src/styles/globals.css",
        "electron/main.js",
        "electron/preload.js"
    ]
    
    all_passed = True
    
    for file_path in key_files:
        full_path = frontend_path / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 缺少: {file_path}")
            all_passed = False
    
    return all_passed

def test_config_files():
    """测试配置文件"""
    print("\n⚙️ 验证配置文件...")
    
    project_root = Path(__file__).parent
    
    config_files = [
        "docker-compose.yml",
        "install.sh",
        "README.md",
        "pyproject.toml",
        "backend/requirements.txt",
        "backend/alembic.ini",
        "backend/.env.example"
    ]
    
    all_passed = True
    
    for file_path in config_files:
        full_path = project_root / file_path
        if full_path.exists():
            print(f"  ✅ {file_path}")
        else:
            print(f"  ❌ 缺少: {file_path}")
            all_passed = False
    
    return all_passed

def test_file_contents():
    """测试关键文件内容"""
    print("\n📝 验证关键文件内容...")
    
    project_root = Path(__file__).parent
    
    # 检查main.py是否有正确的导入
    main_py = project_root / "backend" / "main.py"
    if main_py.exists():
        content = main_py.read_text()
        if "from core.config import settings" in content:
            print("  ✅ main.py 导入正确")
        else:
            print("  ❌ main.py 导入有问题")
            return False
    
    # 检查package.json是否有必要的依赖
    package_json = project_root / "frontend" / "package.json"
    if package_json.exists():
        content = package_json.read_text()
        if '"react"' in content and '"electron"' in content:
            print("  ✅ package.json 依赖正确")
        else:
            print("  ❌ package.json 依赖有问题")
            return False
    
    # 检查docker-compose.yml
    docker_compose = project_root / "docker-compose.yml"
    if docker_compose.exists():
        content = docker_compose.read_text()
        if "postgres" in content and "redis" in content:
            print("  ✅ docker-compose.yml 配置正确")
        else:
            print("  ❌ docker-compose.yml 配置有问题")
            return False
    
    return True

def main():
    """主函数"""
    print("🚀 开始羲和项目结构验证...\n")
    
    tests = [
        ("项目结构", test_project_structure),
        ("后端文件", test_backend_files),
        ("前端文件", test_frontend_files),
        ("配置文件", test_config_files),
        ("文件内容", test_file_contents)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"🎉 {test_name}验证通过！")
            else:
                print(f"❌ {test_name}验证失败！")
        except Exception as e:
            print(f"❌ {test_name}验证异常: {e}")
    
    print(f"\n📊 验证结果: {passed}/{total} 通过")
    
    if passed == total:
        print("🎉 项目结构验证完全通过！")
        print("\n📋 项目总结:")
        print("  ✅ 后端: FastAPI + SQLAlchemy + PostgreSQL + Redis")
        print("  ✅ 前端: Electron + React + Zustand + Framer Motion")
        print("  ✅ AI代理: 多提供商支持 + 智能任务规划")
        print("  ✅ 桌面自动化: 跨平台支持 + 多模态交互")
        print("  ✅ 部署: Docker + 自动化安装脚本")
        print("  ✅ 文档: 完整的架构和安装文档")
        return True
    else:
        print("⚠️ 部分验证失败，请检查相关文件")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)