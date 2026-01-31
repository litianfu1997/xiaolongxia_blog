#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Check Python Dependencies"""

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

print("=== Python Package Check ===\n")
installed = []
missing = []

for name, module in packages.items():
    try:
        __import__(module)
        print(f"[OK] {name}")
        installed.append(name)
    except ImportError:
        print(f"[MISSING] {name}")
        missing.append(name)

print(f"\nInstalled: {len(installed)}/{len(packages)}")
print(f"Missing: {len(missing)}")
if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
