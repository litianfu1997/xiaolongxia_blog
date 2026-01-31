#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试标书生成API
"""
import requests
import json
import sys

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def test_status():
    """测试系统状态"""
    print("=== 测试系统状态 ===\n")
    response = requests.get(f"{API_URL}/api/status")
    data = response.json()

    print(f"数据库: {'✓' if data.get('database') else '✗'}")
    if data.get('database'):
        print(f"  表: {', '.join(data.get('tables', []))}")

    print(f"Milvus: {'✓' if data.get('milvus') else '✗'}")
    print(f"Ollama: {'✓' if data.get('ollama') else '✗'}")
    if data.get('ollama'):
        print(f"  模型: {', '.join(data.get('models', []))}")

    print()

def test_llm():
    """测试LLM"""
    print("=== 测试 LLM ===\n")

    payload = {
        "prompt": "请用一句话介绍你的能力。"
    }

    print("发送提示词...")
    response = requests.post(
        f"{API_URL}/api/test_llm",
        json=payload,
        timeout=60
    )

    data = response.json()

    if data.get('success'):
        print(f"✓ LLM响应成功")
        print(f"\n响应内容:\n{data.get('response')}")
    else:
        print(f"✗ LLM调用失败: {data.get('error')}")

    print()

def test_generate_bid():
    """测试生成标书"""
    print("=== 测试生成标书 ===\n")

    payload = {
        "project_name": "智慧城市综合管理平台",
        "project_description": "建设集交通管理、环境监测、公共安全等功能于一体的智慧城市综合管理平台，实现城市运行态势全面感知、智能分析、协同处置。系统需要支持千万级数据实时处理，提供AI智能分析能力，并确保高可靠性和安全性。",
        "requirements": [
            "系统集成度高，支持多部门数据共享",
            "数据处理能力强，支持千万级数据实时分析",
            "支持移动端访问，响应速度快",
            "具备AI智能分析能力",
            "高可靠性和安全性，符合等保三级要求"
        ]
    }

    print("项目信息:")
    print(f"  名称: {payload['project_name']}")
    print(f"  描述: {payload['project_description'][:50]}...")
    print(f"  需求数量: {len(payload['requirements'])}条")

    print("\n正在生成标书（这可能需要30-60秒）...")
    print("=" * 60)

    try:
        response = requests.post(
            f"{API_URL}/api/generate_bid",
            json=payload,
            timeout=120
        )

        data = response.json()

        if data.get('success'):
            print("\n✓ 标书生成成功！")
            print(f"\n使用资源:")
            print(f"  员工: {data.get('staff_used')}人")
            print(f"  产品: {data.get('products_used')}个")
            print(f"\n生成的标书内容:")
            print("=" * 60)
            print(data.get('bid_document'))
            print("=" * 60)

            # 保存到文件
            filename = "generated_bid_智慧城市.md"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(f"# {payload['project_name']}\n\n")
                f.write(f"## 项目描述\n{payload['project_description']}\n\n")
                f.write(f"## 需求要点\n")
                for req in payload['requirements']:
                    f.write(f"- {req}\n")
                f.write(f"\n## 标书方案\n\n")
                f.write(data.get('bid_document'))

            print(f"\n✓ 标书已保存到: {filename}")

        else:
            print(f"\n✗ 标书生成失败: {data.get('error')}")

    except requests.exceptions.Timeout:
        print("\n✗ 请求超时（120秒）")
    except Exception as e:
        print(f"\n✗ 错误: {e}")

    print()

def test_data():
    """测试数据查询"""
    print("=== 测试数据查询 ===\n")

    # 查询员工
    response = requests.get(f"{API_URL}/api/staff")
    data = response.json()

    if data.get('staff'):
        print(f"✓ 员工数据: {len(data['staff'])}条")
        for staff in data['staff'][:3]:
            print(f"  - {staff['name']} | {staff['title']} | {staff['department']}")

    # 查询产品
    response = requests.get(f"{API_URL}/api/products")
    data = response.json()

    if data.get('products'):
        print(f"\n✓ 产品数据: {len(data['products'])}条")
        for product in data['products'][:3]:
            print(f"  - {product['name']} | {product['category']}")

    print()

def main():
    """主函数"""
    print("🚀 标书智能体 API 测试\n")

    try:
        # 1. 测试系统状态
        test_status()

        # 2. 测试数据查询
        test_data()

        # 3. 测试LLM
        test_llm()

        # 4. 测试生成标书
        test_generate_bid()

        print("\n=== 测试完成 ===")

    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()
