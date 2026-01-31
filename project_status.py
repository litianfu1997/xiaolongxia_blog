#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
项目状态快速检查
"""
import requests
import json
import sys
import io
from datetime import datetime

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_project_status():
    """检查项目状态"""
    print("=" * 80)
    print("🎯 标书智能体项目状态报告")
    print("=" * 80)
    print(f"检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 1. 系统状态
    print("1️⃣ 系统组件状态")
    print("-" * 80)

    try:
        response = requests.get("http://127.0.0.1:5000/api/status", timeout=5)
        status = response.json()

        components = [
            ("数据库 (MySQL)", status.get('database')),
            ("向量库 (Milvus)", status.get('milvus')),
            ("LLM服务 (Ollama)", status.get('ollama')),
        ]

        for name, is_running in components:
            icon = "✅" if is_running else "❌"
            print(f"  {icon} {name}")

        # 功能模块
        print("\n功能模块:")
        modules = status.get('modules', {})
        for name, enabled in modules.items():
            icon = "✅" if enabled else "❌"
            print(f"  {icon} {name}")

    except Exception as e:
        print(f"  ❌ 无法连接到Web服务: {e}")

    # 2. 文件检查
    print("\n2️⃣ 项目文件")
    print("-" * 80)

    import os
    core_files = [
        "app_enhanced.py",
        "vector_store.py",
        "bid_evaluator.py",
        "bid_exporter.py",
        "bid_conversation.py",
        "README.md",
        "API_文档.md",
        "requirements.txt"
    ]

    for filename in core_files:
        exists = os.path.exists(filename)
        icon = "✅" if exists else "❌"
        size = f"{os.path.getsize(filename)} bytes" if exists else "缺失"
        print(f"  {icon} {filename:<30} ({size})")

    # 3. 快速统计
    print("\n3️⃣ 代码统计")
    print("-" * 80)

    total_lines = 0
    total_files = 0

    for filename in os.listdir('.'):
        if filename.endswith('.py') and not filename.startswith('test_') and filename != 'code_quality_check.py':
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    lines = len(f.readlines())
                    total_lines += lines
                    total_files += 1
                    print(f"  {filename:<30} {lines:>5} 行")
            except:
                pass

    print(f"  {'总计':<30} {total_lines:>5} 行 ({total_files} 个文件)")

    # 4. 数据库数据
    print("\n4️⃣ 数据统计")
    print("-" * 80)

    try:
        # 员工数据
        response = requests.get("http://127.0.0.1:5000/api/staff", timeout=5)
        if response.status_code == 200:
            staff_count = len(response.json().get('staff', []))
            print(f"  ✅ 员工数据: {staff_count} 条")
        else:
            print(f"  ❌ 员工数据查询失败")

        # 产品数据
        response = requests.get("http://127.0.0.1:5000/api/products", timeout=5)
        if response.status_code == 200:
            product_count = len(response.json().get('products', []))
            print(f"  ✅ 产品数据: {product_count} 条")
        else:
            print(f"  ❌ 产品数据查询失败")

    except Exception as e:
        print(f"  ❌ 无法查询数据: {e}")

    # 5. Milvus向量库
    print("\n5️⃣ 向量数据库")
    print("-" * 80)

    try:
        from pymilvus import connections, utility

        connections.connect("default", host="localhost", port="19530")
        collections = utility.list_collections()

        if collections:
            print(f"  ✅ 集合数量: {len(collections)}")
            for col in collections:
                print(f"     - {col}")
        else:
            print(f"  ⚠️  无集合数据")

        connections.disconnect("default")

    except Exception as e:
        print(f"  ❌ Milvus连接失败: {e}")

    # 6. 导出的文件
    print("\n6️⃣ 导出文档")
    print("-" * 80)

    export_files = [f for f in os.listdir('.') if f.endswith(('.md', '.docx')) and '20' in f]
    if export_files:
        print(f"  ✅ 最近导出 ({len(export_files)} 个文件):")
        for f in export_files[-5:]:
            print(f"     - {f}")
    else:
        print(f"  ⚠️  无导出文件")

    # 7. 建议
    print("\n7️⃣ 改进建议")
    print("-" * 80)

    suggestions = []

    # 检查是否有.gitignore
    if not os.path.exists('.gitignore'):
        suggestions.append("创建 .gitignore 文件")

    # 检查是否有单元测试
    has_tests = any('test_' in f for f in os.listdir('.'))
    if not has_tests:
        suggestions.append("添加单元测试")

    # 检查是否使用logging
    try:
        with open('app_enhanced.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'import logging' not in content:
                suggestions.append("使用 logging 模块替代 print")
    except:
        pass

    # 检查debug模式
    try:
        with open('app_enhanced.py', 'r', encoding='utf-8') as f:
            content = f.read()
            if 'debug=True' in content:
                suggestions.append("生产环境关闭 debug=True")
    except:
        pass

    if suggestions:
        for i, suggestion in enumerate(suggestions, 1):
            print(f"  {i}. {suggestion}")
    else:
        print(f"  ✅ 无明显问题")

    # 总结
    print("\n" + "=" * 80)
    print("📊 项目健康度评分")
    print("=" * 80)

    score = 0
    max_score = 0

    # 系统组件 (30分)
    if status.get('database'):
        score += 10
    max_score += 10
    if status.get('milvus'):
        score += 10
    max_score += 10
    if status.get('ollama'):
        score += 10
    max_score += 10

    # 文件完整性 (20分)
    if all(os.path.exists(f) for f in core_files[:5]):
        score += 20
    max_score += 20

    # 数据完整性 (20分)
    if staff_count > 0 and product_count > 0:
        score += 20
    max_score += 20

    # 文档完整性 (20分)
    if os.path.exists('README.md') and os.path.exists('API_文档.md'):
        score += 20
    max_score += 20

    # 最佳实践 (10分)
    if len(suggestions) <= 2:
        score += 10
    max_score += 10

    percentage = int(score / max_score * 100) if max_score > 0 else 0

    print(f"\n得分: {score}/{max_score} ({percentage}%)")

    if percentage >= 90:
        grade = "优秀 ✨"
        color = "🟢"
    elif percentage >= 80:
        grade = "良好 👍"
        color = "🟢"
    elif percentage >= 70:
        grade = "合格 ✔️"
        color = "🟡"
    elif percentage >= 60:
        grade = "需改进 ⚠️"
        color = "🟠"
    else:
        grade = "不合格 ❌"
        color = "🔴"

    print(f"评级: {color} {grade}")

    print("\n" + "=" * 80)
    print("✅ 项目状态检查完成")
    print("=" * 80)

if __name__ == '__main__':
    check_project_status()
