#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""检查Python依赖包"""

packages = {
    'python-docx': 'docx',
    'docxtpl': 'docxtpl',
    'pdfplumber': 'pdfplumber',
    'pymilvus': 'pymilvus',
    'sentence-transformers': 'sentence_transformers',
    'openai': 'openai',
    'PyYAML': 'yaml',
    'pandas': 'pandas',
    'numpy': 'numpy',
    'loguru': 'loguru',
    'requests': 'requests',
    'pytest': 'pytest',
    'dotenv': 'dotenv'
}

print("=== Python依赖包检查 ===\n")
installed = []
missing = []

for name, module in packages.items():
    try:
        __import__(module)
        print(f"✅ {name}")
        installed.append(name)
    except ImportError:
        print(f"❌ {name}")
        missing.append(name)

print(f"\n已安装: {len(installed)}/{len(packages)}")
print(f"未安装: {len(missing)}")
if missing:
    print(f"\n缺少的包: {', '.join(missing)}")
