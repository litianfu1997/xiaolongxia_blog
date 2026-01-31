#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""运行标书智能体测试"""
import sys
import os

# 添加code目录到路径
sys.path.insert(0, r'C:\Users\Administrator\Desktop\智能体方案\code')

# 测试导入
print("=== 测试模块导入 ===\n")

try:
    from tender_parser import TenderParser
    print("✓ tender_parser 导入成功")
except Exception as e:
    print(f"✗ tender_parser 导入失败: {e}")

try:
    from format_extractor import FormatExtractor
    print("✓ format_extractor 导入成功")
except Exception as e:
    print(f"✗ format_extractor 导入失败: {e}")

try:
    from generator import HybridGenerator
    print("✓ generator 导入成功")
except Exception as e:
    print(f"✗ generator 导入失败: {e}")

try:
    from format_validator import FormatValidator
    print("✓ format_validator 导入成功")
except Exception as e:
    print(f"✗ format_validator 导入失败: {e}")

try:
    import pymilvus
    print("✓ pymilvus 导入成功")
except Exception as e:
    print(f"✗ pymilvus 导入失败: {e}")

try:
    import sentence_transformers
    print("✓ sentence_transformers 导入成功")
except Exception as e:
    print(f"✗ sentence_transformers 导入失败: {e}")

try:
    import openai
    print("✓ openai 导入成功")
except Exception as e:
    print(f"✗ openai 导入失败: {e}")

try:
    import yaml
    print("✓ yaml 导入成功")
except Exception as e:
    print(f"✗ yaml 导入失败: {e}")

print("\n=== 测试数据库连接 ===\n")

# 测试数据库连接
try:
    import mysql.connector
    conn = mysql.connector.connect(
        host='localhost',
        port=3307,
        user='root',
        password='tender123',
        database='bid_system'
    )
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    print(f"✓ 数据库连接成功")
    print(f"  数据表: {[t[0] for t in tables]}")
    conn.close()
except Exception as e:
    print(f"✗ 数据库连接失败: {e}")

print("\n=== 测试Milvus连接 ===\n")

# 测试Milvus连接
try:
    from pymilvus import connections
    connections.connect(
        alias="default",
        host='localhost',
        port='19530'
    )
    print("✓ Milvus连接成功")
    connections.disconnect("default")
except Exception as e:
    print(f"✗ Milvus连接失败: {e}")

print("\n=== 测试完成 ===")
