#!/usr/bin/env python3
"""
羲和简化测试脚本
不依赖外部包，只测试代码结构和语法
"""

import sys
import os
import ast
from pathlib import Path

def test_python_syntax():
    """测试Python文件语法"""
    print("🔍 测试Python文件语法...")
    
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    
    python_files = [
        "core/config.py",
        "core/database.py", 
        "core/security.py",
        "core/middleware.py",
        "core/monitoring.py",
        "core/exceptions.py",
        "core/ai_providers.py",
        "core/desktop_automation.py",
        "models/user.py",
        "models/task.py",
        "models/agent.py",
        "agents/core/agent.py",
        "agents/implementations/planner_agent.py",
        "agents/implementations/executor_agent.py",
        "services/auth_service.py",
        "services/user_service.py",
        "services/task_service.py",
        "api/v1/auth.py",
        "api/v1/users.py",
        "api/v1/tasks.py",
        "main.py"
    ]
    
    passed = 0
    total = len(python_files)
    
    for file_path in python_files:
        full_path = backend_path / file_path
        if full_path.exists():
            try:
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # 解析Python语法
                ast.parse(content)
                print(f"  ✅ {file_path}")
                passed += 1
                
            except SyntaxError as e:
                print(f"  ❌ {file_path}: 语法错误 - {e}")
            except Exception as e:
                print(f"  ❌ {file_path}: 解析错误 - {e}")
        else:
            print(f"  ❌ {file_path}: 文件不存在")
    
    print(f"\n📊 语法测试结果: {passed}/{total} 通过")
    return passed == total

def test_import_structure():
    """测试导入结构"""
    print("\n🔗 测试导入结构...")
    
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    
    # 检查关键文件的导入
    main_py = backend_path / "main.py"
    if main_py.exists():
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查关键导入
        required_imports = [
            "from core.config import settings",
            "from core.database import init_db",
            "from core.security import setup_security",
            "from api import api_router"
        ]
        
        missing_imports = []
        for import_line in required_imports:
            if import_line not in content:
                missing_imports.append(import_line)
        
        if missing_imports:
            print(f"  ❌ main.py缺少导入: {missing_imports}")
            return False
        else:
            print("  ✅ main.py导入结构正确")
            return True
    else:
        print("  ❌ main.py文件不存在")
        return False

def test_file_structure():
    """测试文件结构"""
    print("\n📁 测试文件结构...")
    
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
            "alembic/"
        ],
        "frontend/": [
            "package.json",
            "src/",
            "electron/"
        ],
        "": [
            "docker-compose.yml",
            "install.sh",
            "README.md"
        ]
    }
    
    all_passed = True
    
    for base_path, items in required_structure.items():
        full_path = project_root / base_path
        print(f"\n📂 检查 {base_path or '根目录'}:")
        
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

def test_config_files():
    """测试配置文件"""
    print("\n⚙️ 测试配置文件...")
    
    project_root = Path(__file__).parent
    
    config_files = [
        "docker-compose.yml",
        "backend/requirements.txt",
        "backend/alembic.ini",
        "frontend/package.json"
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

def test_code_quality():
    """测试代码质量"""
    print("\n🎨 测试代码质量...")
    
    project_root = Path(__file__).parent
    backend_path = project_root / "backend"
    
    # 检查是否有明显的代码问题
    issues = []
    
    # 检查main.py
    main_py = backend_path / "main.py"
    if main_py.exists():
        with open(main_py, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # 检查是否有TODO或FIXME
        if "TODO" in content or "FIXME" in content:
            issues.append("main.py包含TODO或FIXME")
        
        # 检查是否有硬编码
        if "localhost" in content and "0.0.0.0" not in content:
            issues.append("main.py可能包含硬编码的localhost")
    
    if issues:
        for issue in issues:
            print(f"  ⚠️ {issue}")
        return False
    else:
        print("  ✅ 代码质量检查通过")
        return True

def main():
    """主测试函数"""
    print("🚀 开始羲和简化测试...\n")
    
    tests = [
        ("Python语法", test_python_syntax),
        ("导入结构", test_import_structure),
        ("文件结构", test_file_structure),
        ("配置文件", test_config_files),
        ("代码质量", test_code_quality)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                passed += 1
                print(f"🎉 {test_name}测试通过！")
            else:
                print(f"❌ {test_name}测试失败！")
        except Exception as e:
            print(f"❌ {test_name}测试异常: {e}")
    
    print(f"\n📊 测试结果: {passed}/{total} 通过")
    
    if passed == total:
        print("\n🎉 所有测试通过！")
        print("✅ 项目代码结构完整，语法正确")
        print("📝 下一步: 安装依赖包并运行项目")
        print("   1. pip install -r backend/requirements.txt")
        print("   2. cd backend && python main.py")
        return True
    else:
        print("\n⚠️ 部分测试失败，请检查相关文件")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)