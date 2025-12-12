#!/usr/bin/env python3
"""
FinRisk AI Agents 测试脚本
"""

import sys
import os
import requests
import time
from datetime import datetime

def print_header(text):
    """打印标题"""
    print("\n" + "=" * 60)
    print(f" {text}")
    print("=" * 60)

def test_local_server(port=8000):
    """测试本地服务器"""
    print_header("本地服务器测试")
    
    base_url = f"http://localhost:{port}"
    endpoints = [
        ("健康检查", f"{base_url}/health"),
        ("API信息", f"{base_url}/api/info"),
        ("主页", f"{base_url}/"),
        ("Gradio界面", f"{base_url}/app")
    ]
    
    results = []
    
    for name, url in endpoints:
        try:
            start = time.time()
            response = requests.get(url, timeout=10)
            elapsed = time.time() - start
            
            if response.status_code == 200:
                status = "✅"
                message = f"状态码: {response.status_code}, 耗时: {elapsed:.2f}s"
            else:
                status = "⚠️ "
                message = f"状态码: {response.status_code}"
            
            results.append((status, name, url, message))
            
        except Exception as e:
            results.append(("❌", name, url, f"错误: {str(e)}"))
    
    # 打印结果
    for status, name, url, message in results:
        print(f"{status} {name:15} {message}")
    
    return all(r[0] != "❌" for r in results)

def test_imports():
    """测试模块导入"""
    print_header("模块导入测试")
    
    modules_to_test = [
        ("gradio", "gr"),
        ("fastapi", "FastAPI"),
        ("pandas", "pd"),
        ("numpy", "np"),
        ("plotly.graph_objects", "go")
    ]
    
    results = []
    
    for module, alias in modules_to_test:
        try:
            __import__(module.split('.')[0])
            results.append(("✅", module, "导入成功"))
        except ImportError as e:
            results.append(("❌", module, f"导入失败: {e}"))
    
    # 测试自定义模块
    custom_modules = [
        ("src.app", "create_app"),
        ("api.index", "app")
    ]
    
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    
    for module, function in custom_modules:
        try:
            mod = __import__(module)
            results.append(("✅", module, "导入成功"))
        except Exception as e:
            results.append(("❌", module, f"导入失败: {e}"))
    
    for status, module, message in results:
        print(f"{status} {module:20} {message}")
    
    return all(r[0] != "❌" for r in results)

def check_requirements():
    """检查依赖"""
    print_header("依赖检查")
    
    import pkg_resources
    
    with open("requirements.txt", "r") as f:
        required = []
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                # 提取包名（去掉版本号）
                pkg_name = line.split('>=')[0].split('==')[0].strip()
                required.append(pkg_name)
    
    results = []
    
    for pkg in required[:10]:  # 只检查前10个
        try:
            dist = pkg_resources.get_distribution(pkg)
            results.append(("✅", pkg, f"版本: {dist.version}"))
        except pkg_resources.DistributionNotFound:
            results.append(("❌", pkg, "未安装"))
    
    for status, pkg, message in results:
        print(f"{status} {pkg:20} {message}")
    
    return all(r[0] != "❌" for r in results)

def main():
    """主函数"""
    print_header("FinRisk AI Agents 系统测试")
    print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 检查当前目录
    print(f"工作目录: {os.getcwd()}")
    print(f"Python版本: {sys.version}")
    
    tests = [
        ("依赖检查", check_requirements),
        ("模块导入", test_imports),
        ("本地服务器", lambda: test_local_server(8000))
    ]
    
    all_passed = True
    
    for test_name, test_func in tests:
        try:
            passed = test_func()
            if not passed:
                all_passed = False
        except Exception as e:
            print(f"❌ {test_name} 测试异常: {e}")
            all_passed = False
    
    print_header("测试总结")
    
    if all_passed:
        print("🎉 所有测试通过！")
        print("系统可以正常部署到 Vercel")
    else:
        print("⚠️  部分测试失败，请检查以上错误")
        print("建议先解决本地问题再部署")
    
    return 0 if all_passed else 1

if __name__ == "__main__":
    sys.exit(main())
