#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标书质量评估模块
评估生成标书的质量和完整性
"""
import re
import requests
from typing import Dict, List
import json
import io
import sys

class BidEvaluator:
    """标书评估器"""

    def __init__(self, ollama_url="http://localhost:11434", model="qwen2:1.5b"):
        """初始化"""
        self.ollama_url = ollama_url
        self.model = model

    def evaluate_structure(self, bid_content: str) -> Dict:
        """评估结构完整性"""
        required_sections = [
            "项目理解", "需求分析", "技术方案", "系统设计",
            "实施计划", "团队", "质量", "培训", "售后", "资质"
        ]

        found_sections = []
        missing_sections = []

        for section in required_sections:
            if section in bid_content:
                found_sections.append(section)
            else:
                missing_sections.append(section)

        score = len(found_sections) / len(required_sections) * 100

        return {
            "score": round(score, 2),
            "found": found_sections,
            "missing": missing_sections,
            "completeness": "完整" if score >= 80 else "需补充" if score >= 60 else "不完整"
        }

    def evaluate_content_quality(self, bid_content: str) -> Dict:
        """评估内容质量"""
        metrics = {
            "word_count": len(bid_content),
            "paragraph_count": len([p for p in bid_content.split('\n\n') if p.strip()]),
            "has_tables": '│' in bid_content or '|' in bid_content,
            "has_lists": bool(re.search(r'^[\-\*]\s', bid_content, re.MULTILINE)),
            "has_numbers": bool(re.search(r'\d+[\u4e00-\u9fa5]+年', bid_content)),
        }

        # 质量评分
        quality_score = 0
        if metrics["word_count"] > 2000:
            quality_score += 25
        elif metrics["word_count"] > 1000:
            quality_score += 15

        if metrics["paragraph_count"] > 10:
            quality_score += 25
        elif metrics["paragraph_count"] > 5:
            quality_score += 15

        if metrics["has_tables"]:
            quality_score += 15
        if metrics["has_lists"]:
            quality_score += 15
        if metrics["has_numbers"]:
            quality_score += 20

        return {
            "score": quality_score,
            "metrics": metrics,
            "level": "优秀" if quality_score >= 80 else "良好" if quality_score >= 60 else "需改进"
        }

    def evaluate_with_llm(self, bid_content: str, project_requirements: List[str]) -> Dict:
        """使用LLM深度评估"""
        prompt = f"""请评估以下标书方案的质量：

**项目需求：**
{chr(10).join(f"- {r}" for r in project_requirements)}

**标书内容：**
{bid_content[:2000]}

请从以下维度评分（每项0-10分）：
1. 需求覆盖度 - 是否全面响应了项目需求
2. 技术可行性 - 方案是否合理可行
3. 方案完整性 - 是否包含必要的章节和内容
4. 说服力 - 论证是否充分有力
5. 专业性 - 表达是否专业规范

请以JSON格式返回评估结果：
{{
    "需求覆盖度": 分数,
    "技术可行性": 分数,
    "方案完整性": 分数,
    "说服力": 分数,
    "专业性": 分数,
    "总评": "优秀/良好/一般/需改进",
    "建议": "具体改进建议"
}}
"""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                content = result.get('message', {}).get('content', '')

                # 尝试解析JSON
                try:
                    json_match = re.search(r'\{[\s\S]*\}', content)
                    if json_match:
                        eval_result = json.loads(json_match.group())
                        return eval_result
                except:
                    pass

                return {"error": "无法解析评估结果", "raw": content}

        except Exception as e:
            return {"error": str(e)}

    def full_evaluation(self, bid_content: str, project_requirements: List[str] = None) -> Dict:
        """完整评估"""
        # 结构评估
        structure_eval = self.evaluate_structure(bid_content)

        # 内容质量评估
        content_eval = self.evaluate_content_quality(bid_content)

        # 综合评分
        overall_score = (structure_eval["score"] * 0.4 + content_eval["score"] * 0.6)

        result = {
            "structure": structure_eval,
            "content_quality": content_eval,
            "overall_score": round(overall_score, 2),
            "overall_level": self._get_level(overall_score),
            "recommendations": self._generate_recommendations(structure_eval, content_eval)
        }

        # LLM深度评估（如果提供需求）
        if project_requirements:
            llm_eval = self.evaluate_with_llm(bid_content, project_requirements)
            if "error" not in llm_eval:
                result["llm_evaluation"] = llm_eval

        return result

    def _get_level(self, score: float) -> str:
        """获取等级"""
        if score >= 85:
            return "优秀"
        elif score >= 70:
            return "良好"
        elif score >= 60:
            return "合格"
        else:
            return "需改进"

    def _generate_recommendations(self, structure_eval: Dict, content_eval: Dict) -> List[str]:
        """生成改进建议"""
        recommendations = []

        if structure_eval["missing"]:
            recommendations.append(f"建议补充缺失章节：{', '.join(structure_eval['missing'][:3])}")

        if content_eval["metrics"]["word_count"] < 1000:
            recommendations.append("内容偏少，建议扩充各章节内容")

        if not content_eval["metrics"]["has_tables"]:
            recommendations.append("建议添加表格增强可读性")

        if not content_eval["metrics"]["has_lists"]:
            recommendations.append("建议使用列表条理化内容")

        if not recommendations:
            recommendations.append("标书质量良好，可考虑增加具体案例和数据支撑")

        return recommendations

# 测试
if __name__ == '__main__':
    import sys
    import io
    if sys.platform == 'win32':
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    evaluator = BidEvaluator()

    # 测试用例
    sample_bid = """
    # 智慧城市平台技术方案

    ## 一、项目理解与需求分析
    本项目旨在建设智慧城市综合管理平台，实现城市运行态势全面感知。

    ## 二、技术方案
    采用微服务架构，使用Spring Cloud + Vue.js技术栈。
    - 前端：Vue.js 3.0
    - 后端：Spring Boot 2.7
    - 数据库：MySQL 8.0

    ## 三、实施方案
    项目周期12个月，分为需求分析、系统设计、开发实施、测试上线四个阶段。
    团队配置：项目经理1名，架构师1名，开发工程师5名。

    ## 四、质量保障
    建立完善的质量管理体系，通过ISO9001认证，确保项目质量。
    """

    print("=== 标书质量评估测试 ===\n")

    result = evaluator.full_evaluation(
        sample_bid,
        ["系统集成度高", "实时数据处理", "AI智能分析"]
    )

    print(f"结构完整性: {result['structure']['completeness']} ({result['structure']['score']}分)")
    print(f"  找到章节: {len(result['structure']['found'])}个")
    print(f"  缺失章节: {result['structure']['missing'] if result['structure']['missing'] else '无'}")

    print(f"\n内容质量: {result['content_quality']['level']} ({result['content_quality']['score']}分)")
    print(f"  字数: {result['content_quality']['metrics']['word_count']}")
    print(f"  段落: {result['content_quality']['metrics']['paragraph_count']}")

    print(f"\n综合评分: {result['overall_score']}分 - {result['overall_level']}")

    print(f"\n改进建议:")
    for rec in result['recommendations']:
        print(f"  - {rec}")
