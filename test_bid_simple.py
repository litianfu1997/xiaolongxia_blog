#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
简化版标书生成测试
"""
import requests
import json
import sys
import time

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def test_generate_bid_simple():
    """测试生成标书（简化版）"""
    print("=== 测试生成标书（简化版）===\n")

    payload = {
        "project_name": "企业数据中台建设",
        "project_description": "建设企业级数据中台，实现数据统一管理、智能分析和价值挖掘。",
        "requirements": [
            "数据治理能力",
            "BI报表功能",
            "实时数据处理"
        ]
    }

    print(f"项目: {payload['project_name']}")
    print(f"需求: {len(payload['requirements'])}条")
    print("\n开始生成（最长等待3分钟）...")
    print("=" * 60)

    start_time = time.time()

    try:
        response = requests.post(
            f"{API_URL}/api/generate_bid",
            json=payload,
            timeout=200  # 200秒超时
        )

        elapsed = time.time() - start_time
        print(f"\n耗时: {elapsed:.1f}秒")

        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            try:
                data = response.json()

                if data.get('success'):
                    print("\n✅ 标书生成成功！")
                    print(f"使用资源: 员工{data.get('staff_used')}人, 产品{data.get('products_used')}个")
                    print(f"\n标书预览（前500字）:")
                    print("-" * 60)
                    content = data.get('bid_document', '')
                    print(content[:500])
                    if len(content) > 500:
                        print(f"\n... (总共{len(content)}字符)")
                    print("-" * 60)

                    # 保存文件
                    filename = f"bid_{payload['project_name']}.md"
                    with open(filename, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"\n✅ 已保存到: {filename}")

                else:
                    print(f"\n❌ 生成失败: {data.get('error')}")

            except json.JSONDecodeError as e:
                print(f"\n❌ JSON解析错误: {e}")
                print(f"响应内容前200字符:\n{response.text[:200]}")

        else:
            print(f"\n❌ HTTP错误: {response.status_code}")
            print(f"响应内容:\n{response.text[:500]}")

    except requests.exceptions.Timeout:
        elapsed = time.time() - start_time
        print(f"\n❌ 请求超时（{elapsed:.1f}秒）")
    except Exception as e:
        print(f"\n❌ 错误: {e}")

    print()

if __name__ == '__main__':
    test_generate_bid_simple()
