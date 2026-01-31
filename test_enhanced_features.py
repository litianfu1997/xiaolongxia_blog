#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试增强版功能
"""
import requests
import json
import sys
import io

# 设置UTF-8输出
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def test_status():
    """测试系统状态"""
    print("\n=== 1. 系统状态检查 ===\n")
    response = requests.get(f"{API_URL}/api/status")
    data = response.json()

    print(f"数据库: {'✓' if data.get('database') else '✗'}")
    print(f"Milvus: {'✓' if data.get('milvus') else '✗'}")
    print(f"Ollama: {'✓' if data.get('ollama') else '✗'}")

    print("\n功能模块:")
    modules = data.get('modules', {})
    for name, status in modules.items():
        print(f"  {name}: {'✓' if status else '✗'}")

def test_evaluate():
    """测试评估功能"""
    print("\n=== 2. 标书质量评估 ===\n")

    sample_bid = """
    # 智慧城市技术方案

    ## 项目理解
    本项目旨在建设智慧城市综合管理平台

    ## 技术方案
    采用微服务架构，使用Spring Cloud + Vue.js

    ## 实施计划
    项目周期12个月，分为四个阶段

    ## 质量保障
    建立完善的质量管理体系
    """

    payload = {
        "bid_content": sample_bid,
        "requirements": ["系统集成度高", "实时数据处理", "AI智能分析"]
    }

    print("正在评估...")
    response = requests.post(f"{API_URL}/api/evaluate", json=payload, timeout=30)
    data = response.json()

    if data.get('success'):
        eval_result = data['evaluation']
        print(f"✓ 评估成功")
        print(f"  结构完整性: {eval_result['structure']['completeness']} ({eval_result['structure']['score']}分)")
        print(f"  内容质量: {eval_result['content_quality']['level']} ({eval_result['content_quality']['score']}分)")
        print(f"  综合评分: {eval_result['overall_score']}分 - {eval_result['overall_level']}")

        print(f"\n  改进建议:")
        for rec in eval_result['recommendations'][:3]:
            print(f"    - {rec}")
    else:
        print(f"✗ 评估失败: {data.get('error')}")

def test_export():
    """测试导出功能"""
    print("\n=== 3. 标书导出 ===\n")

    sample_bid = """
    # 智慧城市平台标书

    ## 技术方案
    采用微服务架构设计

    ## 实施计划
    项目周期12个月
    """

    metadata = {
        "project_name": "测试项目",
        "company": "测试公司",
        "date": "2026-01-31"
    }

    payload = {
        "bid_content": sample_bid,
        "metadata": metadata,
        "format": "all"
    }

    print("正在导出...")
    response = requests.post(f"{API_URL}/api/export", json=payload, timeout=30)
    data = response.json()

    if data.get('success'):
        result = data['result']
        print(f"✓ 导出成功")
        if result.get('markdown'):
            print(f"  Markdown: {result['markdown']}")
        if result.get('word'):
            print(f"  Word: {result['word']}")
    else:
        print(f"✗ 导出失败: {data.get('error')}")

def test_chat():
    """测试对话功能"""
    print("\n=== 4. 多轮对话 ===\n")

    questions = [
        "你好，我需要编写标书",
        "项目是智慧城市平台"
    ]

    for question in questions:
        print(f"用户: {question}")

        payload = {
            "message": question,
            "context": {}
        }

        response = requests.post(f"{API_URL}/api/chat", json=payload, timeout=30)
        data = response.json()

        if data.get('success'):
            answer = data['response']
            print(f"AI: {answer[:100]}...\n")
        else:
            print(f"✗ 对话失败: {data.get('error')}\n")

def test_vector_search():
    """测试向量检索"""
    print("\n=== 5. 向量检索 ===\n")

    payload = {
        "query": "微服务架构设计",
        "doc_type": "technical_solution",
        "top_k": 3
    }

    print("正在检索...")
    response = requests.post(f"{API_URL}/api/vector/search", json=payload, timeout=30)
    data = response.json()

    if data.get('success'):
        results = data['results']
        print(f"✓ 找到 {len(results)} 条相关内容")
        for i, r in enumerate(results[:2], 1):
            print(f"  {i}. [{r['doc_type']}] {r['content'][:60]}...")
    else:
        print(f"✗ 检索失败: {data.get('error')}")

def main():
    """主函数"""
    print("=" * 60)
    print("🚀 标书智能体增强版功能测试")
    print("=" * 60)

    try:
        test_status()
        test_evaluate()
        test_export()
        test_chat()
        test_vector_search()

        print("\n" + "=" * 60)
        print("✓ 所有测试完成")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
