#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
快速测试qwen2:1.5b模型速度
"""
import requests
import time
import sys

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

API_URL = "http://127.0.0.1:5000"

def test_llm_speed():
    """测试LLM生成速度"""
    print("=== 测试 qwen2:1.5b 模型速度 ===\n")

    payload = {
        "prompt": "请用100字左右介绍什么是人工智能。"
    }

    print(f"提示词: {payload['prompt']}")
    print("\n生成中...")

    start = time.time()
    response = requests.post(
        f"{API_URL}/api/test_llm",
        json=payload,
        timeout=60
    )
    elapsed = time.time() - start

    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            content = data.get('response', '')
            print(f"\n✓ 成功！")
            print(f"耗时: {elapsed:.1f}秒")
            print(f"内容长度: {len(content)} 字符")
            print(f"生成速度: {len(content)/elapsed:.1f} 字符/秒")
            print(f"\n生成内容:\n{'='*60}")
            print(content)
            print('='*60)
        else:
            print(f"\n✗ 失败: {data.get('error')}")
    else:
        print(f"\n✗ HTTP错误: {response.status_code}")

if __name__ == '__main__':
    test_llm_speed()
