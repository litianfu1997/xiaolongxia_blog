#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Test Ollama connection"""
import sys
import json

print("=== Testing Ollama Connection ===\n")

# Test 1: HTTP API
try:
    import requests
    response = requests.get("http://localhost:11434/api/tags")
    if response.status_code == 200:
        models = response.json().get("models", [])
        print(f"[OK] Ollama API is running")
        print(f"Available models:")
        for model in models:
            print(f"  - {model['name']}")
    else:
        print(f"[FAIL] Ollama API returned status {response.status_code}")
except Exception as e:
    print(f"[FAIL] Cannot connect to Ollama API: {e}")

# Test 2: Generate completion
print("\n=== Testing Ollama Generation ===\n")

try:
    import requests
    payload = {
        "model": "qwen3:4b",
        "prompt": "你好，请用一句话介绍你自己。",
        "stream": False
    }
    response = requests.post(
        "http://localhost:11434/api/generate",
        json=payload,
        timeout=30
    )
    if response.status_code == 200:
        result = response.json()
        print(f"[OK] Generation successful")
        print(f"Response: {result.get('response', 'No response')}")
    else:
        print(f"[FAIL] Generation failed with status {response.status_code}")
except Exception as e:
    print(f"[FAIL] Generation error: {e}")

# Test 3: Chat completion (preferred)
print("\n=== Testing Ollama Chat API ===\n")

try:
    import requests
    payload = {
        "model": "qwen3:4b",
        "messages": [
            {"role": "user", "content": "你好，请简单回复：测试成功"}
        ],
        "stream": False
    }
    response = requests.post(
        "http://localhost:11434/api/chat",
        json=payload,
        timeout=30
    )
    if response.status_code == 200:
        result = response.json()
        message = result.get("message", {})
        content = message.get("content", "No response")
        print(f"[OK] Chat API successful")
        print(f"Response: {content}")
    else:
        print(f"[FAIL] Chat API failed with status {response.status_code}")
except Exception as e:
    print(f"[FAIL] Chat API error: {e}")

print("\n=== Test Complete ===")
print("\nConfiguration:")
print("  LLM_BACKEND=ollama")
print("  OLLAMA_BASE_URL=http://localhost:11434")
print("  OLLAMA_MODEL=qwen3:4b")
