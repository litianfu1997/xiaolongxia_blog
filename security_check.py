#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
安全专项检查
"""
import re
import os
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

def check_security_issues():
    """检查安全问题"""
    print("=" * 80)
    print("🔒 安全专项检查")
    print("=" * 80)

    files_to_check = [
        'app_enhanced.py',
        'vector_store.py',
        'bid_evaluator.py',
        'bid_exporter.py',
        'bid_conversation.py',
        'app.py'
    ]

    security_issues = []

    for filename in files_to_check:
        if not os.path.exists(filename):
            continue

        print(f"\n检查: {filename}")
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.split('\n')

        # 1. SQL注入检查
        sql_patterns = [
            r'execute\s*\(\s*["\'][^"]*\+',
            r'execute\s*\(\s*f["\'].*?\{.*?\}',
            r'execute\s*\(\s*"%.*?%.*?"'
        ]
        for i, line in enumerate(lines, 1):
            for pattern in sql_patterns:
                if re.search(pattern, line) and 'format' not in line:
                    if 'cursor.execute' in line or 'conn.execute' in line:
                        # 排除参数化查询
                        if '%s' not in line and '$1' not in line:
                            security_issues.append({
                                'file': filename,
                                'line': i,
                                'type': 'SQL Injection',
                                'level': 'CRITICAL',
                                'content': line.strip()
                            })

        # 2. 硬编码密钥检查
        secret_patterns = [
            (r'password\s*=\s*["\'][^"\']{8,}["\']', 'Hardcoded Password'),
            (r'api_key\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded API Key'),
            (r'secret\s*=\s*["\'][^"\']{16,}["\']', 'Hardcoded Secret'),
            (r'token\s*=\s*["\'][^"\']{20,}["\']', 'Hardcoded Token'),
        ]
        for i, line in enumerate(lines, 1):
            for pattern, issue_type in secret_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    # 排除示例和注释
                    if 'example' not in line.lower() and 'test' not in line.lower():
                        security_issues.append({
                            'file': filename,
                            'line': i,
                            'type': issue_type,
                            'level': 'HIGH',
                            'content': line.strip()[:60]
                        })

        # 3. 不安全的反序列化
        if 'pickle.loads' in content or 'cPickle' in content:
            security_issues.append({
                'file': filename,
                'line': content.find('pickle'),
                'type': 'Unsafe Deserialization',
                'level': 'CRITICAL',
                'content': '使用 pickle 模块'
            })

        # 4. 弱加密算法
        weak_crypto = ['md5', 'sha1', 'des3']
        for algo in weak_crypto:
            if f'hashlib.{algo}' in content:
                security_issues.append({
                    'file': filename,
                    'type': 'Weak Cryptography',
                    'level': 'MEDIUM',
                    'content': f'使用弱加密算法: {algo}'
                })

        # 5. 命令注入
        if re.search(r'os\.system\s*\(', content) or re.search(r'subprocess\.call\s*\(', content):
            for i, line in enumerate(lines, 1):
                if 'os.system' in line or 'subprocess.call' in line:
                    if 'shell=True' in line or any(var in line for var in ['os.system', 'subprocess.call']):
                        security_issues.append({
                            'file': filename,
                            'line': i,
                            'type': 'Command Injection',
                            'level': 'HIGH',
                            'content': line.strip()[:60]
                        })

        # 6. 调试信息泄露
        debug_patterns = [
            r'print\s*\(\s*.*password',
            r'print\s*\(\s*.*token',
            r'pprint\(\s*.*request',
            r'app\.run\s*\(\s*.*debug=True'
        ]
        for i, line in enumerate(lines, 1):
            for pattern in debug_patterns:
                if re.search(pattern, line, re.IGNORECASE):
                    security_issues.append({
                        'file': filename,
                        'line': i,
                        'type': 'Debug Information Leak',
                        'level': 'MEDIUM',
                        'content': line.strip()[:60]
                    })

        # 7. 不安全的随机数
        if 'import random' in content and 'random.random()' in content:
            if 'secrets' not in content:
                security_issues.append({
                    'file': filename,
                    'type': 'Weak Random Number Generator',
                    'level': 'LOW',
                    'content': '使用 random 模块生成安全敏感数据'
                })

    # 报告结果
    print(f"\n发现 {len(security_issues)} 个潜在安全问题\n")

    if not security_issues:
        print("✅ 未发现明显安全问题！")
    else:
        # 按级别分组
        by_level = {'CRITICAL': [], 'HIGH': [], 'MEDIUM': [], 'LOW': []}
        for issue in security_issues:
            by_level[issue['level']].append(issue)

        for level in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW']:
            issues = by_level[level]
            if issues:
                icons = {'CRITICAL': '🔴', 'HIGH': '🟠', 'MEDIUM': '🟡', 'LOW': '🔵'}
                print(f"\n{icons[level]} {level} ({len(issues)}个):")
                for issue in issues:
                    print(f"  [{issue['file']}:{issue.get('line', '?')}] {issue['type']}")
                    if 'content' in issue:
                        print(f"    → {issue['content']}")

    # 安全最佳实践检查
    print(f"\n{'=' * 80}")
    print("📋 安全最佳实践检查")
    print(f"{'=' * 80}\n")

    best_practices = {
        '参数化SQL查询': False,
        '环境变量配置': False,
        'HTTPS支持': False,
        '输入验证': False,
        '错误处理': False
    }

    for filename in files_to_check:
        if not os.path.exists(filename):
            continue

        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()

        # 检查参数化查询
        if '%s' in content or '?s' in content or 'cursor.execute' in content:
            if 'execute(%s' in content or 'execute(?, ' in content:
                best_practices['参数化SQL查询'] = True

        # 检查环境变量
        if 'os.getenv' in content or 'os.environ' in content:
            best_practices['环境变量配置'] = True

        # 检查HTTPS
        if 'ssl_context' in content or 'HTTPS' in content:
            best_practices['HTTPS支持'] = True

        # 检查输入验证
        if 'request.json' in content or 'request.form' in content:
            if '.get(' in content or 'if not' in content:
                best_practices['输入验证'] = True

        # 检查错误处理
        if 'try:' in content and 'except' in content:
            best_practices['错误处理'] = True

    for practice, status in best_practices.items():
        icon = '✅' if status else '⚠️'
        print(f"  {icon} {practice}")

    print(f"\n{'=' * 80}")
    print("💡 安全建议")
    print(f"{'=' * 80}\n")

    recommendations = [
        "1. 使用环境变量或配置文件管理敏感信息",
        "2. 生产环境关闭 Flask debug 模式",
        "3. 添加 API 速率限制防止滥用",
        "4. 使用 HTTPS 加密传输",
        "5. 实施请求验证和清洗",
        "6. 添加 CORS 策略限制跨域访问",
        "7. 定期更新依赖包修复漏洞",
        "8. 实施日志记录和监控"
    ]

    for rec in recommendations:
        print(f"  {rec}")

if __name__ == '__main__':
    check_security_issues()
