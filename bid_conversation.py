#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标书多轮对话模块
支持交互式完善标书内容
"""
import requests
import json
from typing import List, Dict, Optional
from datetime import datetime
import io
import sys

class BidConversation:
    """标书对话管理器"""

    def __init__(self, ollama_url="http://localhost:11434", model="qwen2:1.5b"):
        """初始化"""
        self.ollama_url = ollama_url
        self.model = model
        self.conversation_history = []
        self.bid_state = {
            "project_name": "",
            "project_description": "",
            "requirements": [],
            "current_bid": "",
            "metadata": {}
        }

    def add_message(self, role: str, content: str):
        """添加消息到对话历史"""
        self.conversation_history.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })

    def chat(self, user_input: str, context: Dict = None) -> str:
        """与AI对话"""
        # 构建系统提示
        system_prompt = self._build_system_prompt(context)

        # 构建消息列表
        messages = [{"role": "system", "content": system_prompt}]

        # 添加最近的历史（限制数量）
        recent_history = self.conversation_history[-10:] if len(self.conversation_history) > 10 else self.conversation_history
        messages.extend([{"role": m["role"], "content": m["content"]} for m in recent_history])

        # 添加当前用户输入
        messages.append({"role": "user", "content": user_input})

        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": messages,
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                assistant_message = result.get('message', {}).get('content', '')

                # 保存对话
                self.add_message("user", user_input)
                self.add_message("assistant", assistant_message)

                return assistant_message
            else:
                return f"错误：API调用失败 ({response.status_code})"

        except Exception as e:
            return f"错误：{str(e)}"

    def _build_system_prompt(self, context: Dict = None) -> str:
        """构建系统提示"""
        prompt = """你是一个专业的标书编写助手，擅长帮助用户创建和完善标书方案。

你的能力包括：
1. 分析项目需求，提取关键要点
2. 生成专业的标书内容
3. 根据用户反馈修改和完善方案
4. 提供专业的建议和最佳实践

对话原则：
- 简洁专业，避免废话
- 针对性强，直击要点
- 主动引导用户完善信息
- 提供可操作的建议
"""

        if context and context.get('bid_state'):
            bid_state = context['bid_state']
            if bid_state.get('project_name'):
                prompt += f"\n当前项目：{bid_state['project_name']}"
            if bid_state.get('requirements'):
                prompt += f"\n需求要点：{', '.join(bid_state['requirements'][:5])}"

        return prompt

    def refine_bid_section(self, section_name: str, current_content: str, feedback: str) -> str:
        """完善标书章节"""
        prompt = f"""请根据用户反馈完善以下标书章节：

**章节名称：** {section_name}

**当前内容：**
{current_content}

**用户反馈：**
{feedback}

请生成修改后的完整章节内容，要求：
1. 直接反馈修改后的内容，不要解释
2. 保持Markdown格式
3. 突出改进点
4. 内容更加专业和具体
"""

        system_prompt = "你是标书编写专家，擅长根据反馈改进标书内容。"

        try:
            response = requests.post(
                f"{self.ollama_url}/api/chat",
                json={
                    "model": self.model,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ],
                    "stream": False
                },
                timeout=60
            )

            if response.status_code == 200:
                result = response.json()
                return result.get('message', {}).get('content', current_content)

        except Exception as e:
            print(f"警告：完善章节失败 - {e}")

        return current_content

    def interactive_bid_generation(self, project_info: Dict) -> Dict:
        """交互式生成标书"""
        print("\n=== 交互式标书生成 ===\n")

        # 初始化项目信息
        self.bid_state['project_name'] = project_info.get('project_name', '')
        self.bid_state['project_description'] = project_info.get('project_description', '')
        self.bid_state['requirements'] = project_info.get('requirements', [])

        print(f"项目：{self.bid_state['project_name']}")
        print(f"描述：{self.bid_state['project_description'][:80]}...")
        print(f"需求：{len(self.bid_state['requirements'])}条\n")

        # 生成初始标书
        print("正在生成初始标书...")
        # 这里应该调用生成API，简化处理返回占位符
        initial_bid = "# 标书方案\n\n（初始生成内容...）"
        self.bid_state['current_bid'] = initial_bid

        return {
            "success": True,
            "bid": initial_bid,
            "state": self.bid_state
        }

    def save_conversation(self, filepath: str):
        """保存对话历史"""
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump({
                    "conversation_history": self.conversation_history,
                    "bid_state": self.bid_state,
                    "timestamp": datetime.now().isoformat()
                }, f, ensure_ascii=False, indent=2)
            print(f"✓ 对话已保存: {filepath}")
        except Exception as e:
            print(f"✗ 保存失败: {e}")

    def load_conversation(self, filepath: str):
        """加载对话历史"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.conversation_history = data.get('conversation_history', [])
                self.bid_state = data.get('bid_state', {})
            print(f"✓ 对话已加载: {filepath}")
            return True
        except Exception as e:
            print(f"✗ 加载失败: {e}")
            return False

    def get_summary(self) -> Dict:
        """获取对话摘要"""
        user_messages = [m for m in self.conversation_history if m["role"] == "user"]
        assistant_messages = [m for m in self.conversation_history if m["role"] == "assistant"]

        return {
            "total_messages": len(self.conversation_history),
            "user_messages": len(user_messages),
            "assistant_messages": len(assistant_messages),
            "project_name": self.bid_state.get('project_name', '未设置'),
            "has_bid": bool(self.bid_state.get('current_bid'))
        }

# 测试
if __name__ == '__main__':
    conv = BidConversation()

    print("=== 标书对话测试 ===\n")

    # 模拟对话
    test_questions = [
        "你好，我需要为智慧城市项目编写标书",
        "项目需要包含交通管理、环境监测、公共安全三个模块",
        "技术方案应该采用微服务架构",
        "请帮我完善团队配置部分"
    ]

    for i, question in enumerate(test_questions, 1):
        print(f"\n[用户问{i}]: {question}")
        response = conv.chat(question)
        print(f"[AI答]: {response[:150]}...")

    print("\n=== 对话摘要 ===")
    summary = conv.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")

    # 保存对话
    conv.save_conversation("test_conversation.json")
