#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
测试标书生成（使用qwen2:1.5b）
"""
import requests
import time
import sys

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def generate_bid():
    """生成标书"""
    print("=== 生成标书测试（qwen2:1.5b）===\n")

    payload = {
        "project_name": "智慧城市综合管理平台",
        "project_description": "建设集交通管理、环境监测、公共安全等功能于一体的智慧城市综合管理平台。",
        "requirements": [
            "系统集成度高",
            "实时数据处理",
            "AI智能分析",
            "高可靠性"
        ]
    }

    print(f"项目: {payload['project_name']}")
    print(f"需求: {len(payload['requirements'])}条\n")

    print("生成中（最长等待120秒）...")
    print("=" * 60)

    start = time.time()
    try:
        response = requests.post(
            f"{API_URL}/api/generate_bid",
            json=payload,
            timeout=120
        )
        elapsed = time.time() - start

        print(f"\n耗时: {elapsed:.1f}秒")
        print(f"状态码: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                content = data.get('bid_document', '')
                print(f"\n✅ 生成成功！")
                print(f"使用资源: 员工{data.get('staff_used')}人, 产品{data.get('products_used')}个")
                print(f"生成内容长度: {len(content)} 字符")
                print(f"生成速度: {len(content)/elapsed:.1f} 字符/秒")
                print(f"\n标书内容（前800字）:")
                print("=" * 60)
                print(content[:800])
                if len(content) > 800:
                    print(f"\n... (总共{len(content)}字符)")
                print("=" * 60)

                # 保存到文件
                filename = "bid_智慧城市_qwen2-1.5b.md"
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(f"# {payload['project_name']}\n\n")
                    f.write(content)
                print(f"\n✅ 已保存到: {filename}")

            else:
                print(f"\n❌ 失败: {data.get('error')}")
        else:
            print(f"\n❌ HTTP错误: {response.status_code}")

    except requests.exceptions.Timeout:
        elapsed = time.time() - start
        print(f"\n❌ 超时（{elapsed:.1f}秒）")
    except Exception as e:
        print(f"\n❌ 错误: {e}")

if __name__ == '__main__':
    generate_bid()
