#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test system components"""
import sys

print("=== Python Dependencies Test ===\n")

# Test 1: Python packages
packages = {
    'docx': 'python-docx',
    'docxtpl': 'docxtpl',
    'pdfplumber': 'pdfplumber',
    'pymilvus': 'pymilvus',
    'sentence_transformers': 'sentence-transformers',
    'openai': 'openai',
    'yaml': 'PyYAML',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'loguru': 'loguru',
    'requests': 'requests',
    'pytest': 'pytest',
    'dotenv': 'python-dotenv'
}

installed = []
failed = []

for module, package in packages.items():
    try:
        __import__(module)
        print(f"[OK] {package}")
        installed.append(package)
    except Exception as e:
        print(f"[FAIL] {package}: {e}")
        failed.append(package)

print(f"\nInstalled: {len(installed)}/{len(packages)}")
print(f"Failed: {len(failed)}")

# Test 2: Database connection
print("\n=== Database Connection Test ===\n")

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
    print(f"[OK] Database connected")
    print(f"Tables: {[t[0] for t in tables]}")
    conn.close()
except Exception as e:
    print(f"[FAIL] Database: {e}")

# Test 3: Milvus connection
print("\n=== Milvus Connection Test ===\n")

try:
    from pymilvus import connections
    connections.connect(
        alias="default",
        host='localhost',
        port='19530'
    )
    print(f"[OK] Milvus connected")
    connections.disconnect("default")
except Exception as e:
    print(f"[FAIL] Milvus: {e}")

print("\n=== Test Complete ===")
