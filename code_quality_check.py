#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标书智能体项目代码质量检查
"""
import ast
import re
import os
from typing import List, Dict, Tuple
import sys
import io

if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

class CodeChecker:
    """代码检查器"""

    def __init__(self):
        self.issues = []
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'total_functions': 0,
            'total_classes': 0,
        }

    def check_file(self, filepath: str) -> Dict:
        """检查单个文件"""
        issues = []
        metrics = {
            'filepath': filepath,
            'lines': 0,
            'functions': 0,
            'classes': 0,
            'complexity': 0,
            'has_docstring': False,
            'has_encoding': False,
            'issues': []
        }

        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')
                metrics['lines'] = len(lines)

            # 检查编码声明
            if any(line.startswith('# -*- coding:') for line in lines[:5]):
                metrics['has_encoding'] = True
            else:
                issues.append({
                    'type': 'warning',
                    'level': 'minor',
                    'message': '缺少编码声明（建议添加：# -*- coding: utf-8 -*-）'
                })

            # 解析AST
            try:
                tree = ast.parse(content)

                # 统计函数和类
                for node in ast.walk(tree):
                    if isinstance(node, ast.FunctionDef):
                        metrics['functions'] += 1
                    elif isinstance(node, ast.ClassDef):
                        metrics['classes'] += 1

                # 检查模块docstring
                if (tree.body and
                    isinstance(tree.body[0], ast.Expr) and
                    isinstance(tree.body[0].value, ast.Constant)):
                    metrics['has_docstring'] = True

            except SyntaxError as e:
                issues.append({
                    'type': 'error',
                    'level': 'critical',
                    'message': f'语法错误: {e}'
                })

            # 检查潜在问题
            issues.extend(self._check_code_patterns(content, filepath))

            metrics['issues'] = issues
            self.stats['total_files'] += 1
            self.stats['total_lines'] += metrics['lines']
            self.stats['total_functions'] += metrics['functions']
            self.stats['total_classes'] += metrics['classes']

        except Exception as e:
            issues.append({
                'type': 'error',
                'level': 'critical',
                'message': f'无法读取文件: {e}'
            })

        return metrics

    def _check_code_patterns(self, content: str, filepath: str) -> List[Dict]:
        """检查代码模式"""
        issues = []

        # 检查硬编码敏感信息
        if 'password' in content.lower() or 'api_key' in content.lower():
            if re.search(r'(password|api_key)\s*=\s*["\'][^"\']+["\']', content, re.IGNORECASE):
                # 排除示例和注释
                if 'example' not in filepath.lower() and 'test' not in filepath.lower():
                    issues.append({
                        'type': 'security',
                        'level': 'high',
                        'message': '发现可能的硬编码敏感信息（password/api_key）'
                    })

        # 检查TODO/FIXME
        todos = re.findall(r'#\s*(TODO|FIXME|XXX|HACK):?\s*(.+)', content, re.IGNORECASE)
        if todos:
            for keyword, text in todos:
                issues.append({
                    'type': 'todo',
                    'level': 'info',
                    'message': f'{keyword}: {text.strip()}'
                })

        # 检查print语句（生产代码应使用logging）
        if re.search(r'^\s*print\s*\(', content, re.MULTILINE):
            if filepath not in ['test_enhanced_features.py', 'test_bid_api.py']:
                issues.append({
                    'type': 'code_quality',
                    'level': 'minor',
                    'message': '建议使用logging代替print'
                })

        # 检查过长函数（简单估计）
        function_blocks = re.findall(r'def\s+\w+\([^)]*\):(?:\n(?:\s{4,}.*)*)*', content)
        for block in function_blocks:
            lines = block.split('\n')
            if len(lines) > 50:
                func_name = re.search(r'def\s+(\w+)', block)
                if func_name:
                    issues.append({
                        'type': 'complexity',
                        'level': 'medium',
                        'message': f'函数 {func_name.group(1)} 过长（{len(lines)}行），建议拆分'
                    })

        # 检查异常处理
        if 'except:' in content or 'except Exception:' in content:
            if content.count('except Exception:') > 3:
                issues.append({
                    'type': 'best_practice',
                    'level': 'minor',
                    'message': '频繁使用通用异常捕获，建议指定具体异常类型'
                })

        # 检查SQL注入风险
        if re.search(r'execute\s*\(\s*["\'][^"]*\+', content):
            issues.append({
                'type': 'security',
                'level': 'critical',
                'message': '可能的SQL注入风险：使用字符串拼接构建SQL'
            })

        # 检查未使用的导入（简单检查）
        imports = re.findall(r'^from\s+(\S+)\s+import|^import\s+(\S+)', content, re.MULTILINE)
        # 这是一个简单检查，实际需要更复杂的分析

        return issues

    def check_all_files(self, pattern: str = "*.py") -> List[Dict]:
        """检查所有Python文件"""
        results = []

        # 获取所有.py文件
        for filename in os.listdir('.'):
            if filename.endswith('.py') and not filename.startswith('test_'):
                result = self.check_file(filename)
                results.append(result)

        return results

def print_report(results: List[Dict], stats: Dict):
    """打印检查报告"""
    print("=" * 80)
    print("📊 标书智能体代码质量检查报告")
    print("=" * 80)

    # 统计信息
    print(f"\n📈 项目统计:")
    print(f"  总文件数: {stats['total_files']}")
    print(f"  总代码行: {stats['total_lines']}")
    print(f"  函数数: {stats['total_functions']}")
    print(f"  类数: {stats['total_classes']}")
    print(f"  平均每文件行数: {stats['total_lines'] // stats['total_files'] if stats['total_files'] else 0}")

    # 问题汇总
    all_issues = []
    for result in results:
        all_issues.extend(result['issues'])

    print(f"\n⚠️  问题汇总 (共{len(all_issues)}个):")

    # 按级别分组
    by_level = {'critical': [], 'high': [], 'medium': [], 'minor': [], 'info': []}
    for issue in all_issues:
        by_level[issue['level']].append(issue)

    for level in ['critical', 'high', 'medium', 'minor', 'info']:
        issues = by_level[level]
        if issues:
            icons = {
                'critical': '🔴',
                'high': '🟠',
                'medium': '🟡',
                'minor': '🟢',
                'info': '🔵'
            }
            print(f"\n{icons[level]} {level.upper()} ({len(issues)}个):")
            for issue in issues[:5]:  # 只显示前5个
                print(f"  - [{issue['type']}] {issue['message']}")
            if len(issues) > 5:
                print(f"  ... 还有{len(issues) - 5}个")

    # 详细文件报告
    print(f"\n📁 文件详情:")
    for result in results:
        filename = os.path.basename(result['filepath'])
        issues_count = len(result['issues'])

        if issues_count > 0:
            print(f"\n  {filename} ({result['lines']}行, {result['functions']}函数, {result['classes']}类)")
            for issue in result['issues'][:3]:
                print(f"    - [{issue['level']}] {issue['message']}")
            if len(result['issues']) > 3:
                print(f"    ... 还有{len(result['issues']) - 3}个问题")

    # 评分
    critical = len(by_level['critical'])
    high = len(by_level['high'])
    medium = len(by_level['medium'])

    score = 100 - (critical * 20 + high * 10 + medium * 5)
    score = max(0, score)

    print(f"\n{'=' * 80}")
    print(f"📊 代码质量评分: {score}/100")

    if score >= 90:
        grade = "优秀 ✨"
    elif score >= 80:
        grade = "良好 👍"
    elif score >= 70:
        grade = "合格 ✔️"
    elif score >= 60:
        grade = "需改进 ⚠️"
    else:
        grade = "不合格 ❌"

    print(f"评级: {grade}")
    print(f"{'=' * 80}")

    # 改进建议
    if critical > 0 or high > 0:
        print(f"\n💡 优先改进建议:")
        if critical > 0:
            print(f"  1. 🔴 立即修复{critical}个严重问题")
        if high > 0:
            print(f"  2. 🟠 尽快解决{high}个高风险问题")
        if 'print' in str([i['message'] for i in all_issues]):
            print(f"  3. 用logging替换print语句")
        if 'SQL' in str([i['message'] for i in all_issues]):
            print(f"  4. 修复SQL注入风险")

if __name__ == '__main__':
    checker = CodeChecker()

    # 核心模块列表
    core_files = [
        'app_enhanced.py',
        'vector_store.py',
        'bid_evaluator.py',
        'bid_exporter.py',
        'bid_conversation.py',
        'app.py'
    ]

    print("正在检查核心模块...\n")

    results = []
    for filename in core_files:
        if os.path.exists(filename):
            result = checker.check_file(filename)
            results.append(result)

    print_report(results, checker.stats)
