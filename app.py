#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标书智能体 Web 应用
简单的Web界面用于测试标书生成功能
"""
from flask import Flask, render_template, request, jsonify
import mysql.connector
from pymilvus import connections, Collection
import requests
import json
from datetime import datetime
import os

app = Flask(__name__)

# 配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'tender123',
    'database': 'bid_system'
}

MILVUS_CONFIG = {
    'host': 'localhost',
    'port': '19530'
}

OLLAMA_CONFIG = {
    'base_url': 'http://localhost:11434',
    'model': 'qwen2:1.5b'  # 使用更快的模型
}

def get_db_connection():
    """获取数据库连接"""
    return mysql.connector.connect(**DB_CONFIG)

def get_milvus_connection():
    """获取Milvus连接"""
    if not connections.has_connection("default"):
        connections.connect(
            alias="default",
            host=MILVUS_CONFIG['host'],
            port=MILVUS_CONFIG['port']
        )
    return connections

def query_ollama(prompt, system_prompt=None):
    """调用Ollama API"""
    messages = []
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    messages.append({"role": "user", "content": prompt})

    try:
        response = requests.post(
            f"{OLLAMA_CONFIG['base_url']}/api/chat",
            json={
                "model": OLLAMA_CONFIG['model'],
                "messages": messages,
                "stream": False
            },
            timeout=180  # 增加到3分钟
        )

        if response.status_code == 200:
            result = response.json()
            content = result.get('message', {}).get('content', '')
            if content:
                return content
            else:
                print(f"警告：Ollama返回空内容")
                return None
        else:
            print(f"错误：Ollama返回状态码 {response.status_code}")
            print(f"响应内容：{response.text[:500]}")
            return None

    except requests.exceptions.Timeout:
        print("错误：Ollama请求超时（180秒）")
        return None
    except Exception as e:
        print(f"错误：调用Ollama失败 - {e}")
        return None

def load_bid_template():
    """加载标书模板"""
    try:
        with open('bid_template.md', 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return None

@app.route('/')
def index():
    """首页"""
    return render_template('index.html')

@app.route('/api/status')
def status():
    """系统状态"""
    status_info = {
        'database': False,
        'milvus': False,
        'ollama': False,
        'timestamp': datetime.now().isoformat()
    }

    # 检查数据库
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SHOW TABLES")
        tables = [t[0] for t in cursor.fetchall()]
        conn.close()
        status_info['database'] = True
        status_info['tables'] = tables
    except Exception as e:
        status_info['database_error'] = str(e)

    # 检查Milvus
    try:
        get_milvus_connection()
        status_info['milvus'] = True
    except Exception as e:
        status_info['milvus_error'] = str(e)

    # 检查Ollama
    try:
        response = requests.get(f"{OLLAMA_CONFIG['base_url']}/api/tags", timeout=5)
        if response.status_code == 200:
            status_info['ollama'] = True
            models = response.json().get('models', [])
            status_info['models'] = [m['name'] for m in models]
    except Exception as e:
        status_info['ollama_error'] = str(e)

    return jsonify(status_info)

@app.route('/api/staff', methods=['GET', 'POST'])
def staff():
    """员工信息"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        # 查询员工
        cursor.execute("SELECT * FROM staff LIMIT 50")
        staff_list = cursor.fetchall()
        conn.close()
        return jsonify({'staff': staff_list})

    elif request.method == 'POST':
        # 添加员工
        data = request.json
        cursor.execute("""
            INSERT INTO staff (employee_id, name, title, department, education,
                             specialization, experience, phone, email, skills)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data.get('employee_id'),
            data.get('name'),
            data.get('title'),
            data.get('department'),
            data.get('education'),
            data.get('specialization'),
            data.get('experience', 0),
            data.get('phone'),
            data.get('email'),
            json.dumps(data.get('skills', []), ensure_ascii=False)
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': cursor.lastrowid})

@app.route('/api/products', methods=['GET', 'POST'])
def products():
    """产品信息"""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'GET':
        cursor.execute("SELECT * FROM products LIMIT 50")
        product_list = cursor.fetchall()
        conn.close()
        return jsonify({'products': product_list})

    elif request.method == 'POST':
        data = request.json
        cursor.execute("""
            INSERT INTO products (product_code, name, category, specifications,
                                description, manufacturer)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data.get('product_code'),
            data.get('name'),
            data.get('category'),
            data.get('specifications'),
            data.get('description'),
            data.get('manufacturer')
        ))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'id': cursor.lastrowid})

@app.route('/api/generate_bid', methods=['POST'])
def generate_bid():
    """生成标书"""
    data = request.json

    # 获取项目信息
    project_name = data.get('project_name', '')
    project_description = data.get('project_description', '')
    requirements = data.get('requirements', [])

    # 查询相关数据
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 获取可用员工
    cursor.execute("SELECT * FROM staff WHERE is_available = TRUE LIMIT 10")
    staff_list = cursor.fetchall()

    # 获取可用产品
    cursor.execute("SELECT * FROM products WHERE is_available = TRUE LIMIT 10")
    product_list = cursor.fetchall()

    conn.close()

    # 加载标书模板
    template = load_bid_template()

    # 构建提示词
    prompt = f"""
请根据以下信息生成一份专业标书方案：

**项目名称：** {project_name}

**项目描述：**
{project_description}

**需求要点：**
{chr(10).join(f"- {r}" for r in requirements)}

**可用人员（{len(staff_list)}人）：**
{chr(10).join(f"- {s['name']} ({s['title']}, {s['department']}, {s['experience']}年经验, 技能: {s.get('skills', [])})" for s in staff_list[:8])}

**可用产品（{len(product_list)}个）：**
{chr(10).join(f"- {p['name']} ({p['category']}: {p.get('description', 'N/A')})" for p in product_list[:8])}

**公司资质：**
- CMMI 5级认证
- ISO9001质量管理体系
- ISO27001信息安全管理体系
- 信息系统集成及服务一级资质
- 高新技术企业

请生成一份结构完整、专业的标书方案，包括以下部分：
1. 项目理解与需求分析
2. 总体技术方案
3. 系统功能设计
4. 团队配置与人员安排
5. 项目实施计划
6. 质量保障与风险控制
7. 售后服务与培训方案

要求：
- 突出技术优势和创新点
- 体现公司实力和经验
- 方案具体可行，有说服力
- 格式清晰，层次分明
"""

    system_prompt = """你是一个资深的标书编写专家，拥有20年IT项目投标经验。
你擅长根据项目需求、公司资源和行业最佳实践，生成专业、详细、有竞争力的标书方案。
你的标书总是能够准确把握客户需求，突出技术优势，展示公司实力，提高中标率。
输出格式：使用Markdown格式，结构清晰，层次分明，重点突出。"""

    # 调用LLM
    response = query_ollama(prompt, system_prompt)

    if response:
        return jsonify({
            'success': True,
            'bid_document': response,
            'staff_used': len(staff_list),
            'products_used': len(product_list)
        })
    else:
        return jsonify({
            'success': False,
            'error': '生成失败，请检查Ollama服务'
        }), 500

@app.route('/api/test_llm', methods=['POST'])
def test_llm():
    """测试LLM"""
    data = request.json
    prompt = data.get('prompt', '你好，请简单介绍一下你自己。')

    response = query_ollama(prompt)

    if response:
        return jsonify({
            'success': True,
            'response': response
        })
    else:
        return jsonify({
            'success': False,
            'error': 'LLM调用失败'
        }), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
