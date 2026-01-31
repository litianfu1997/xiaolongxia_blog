# 标书智能体 - AI驱动的标书自动生成系统

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> 🤖 基于大语言模型的智能标书生成平台，支持质量评估、多轮对话、向量检索、Word导出

---

## ✨ 特性

### 核心功能
- **🚀 标书生成** - 基于项目需求自动生成专业标书方案
- **📊 质量评估** - 自动评估结构完整性和内容质量
- **💬 多轮对话** - 交互式完善标书内容
- **🔍 向量检索** - 基于语义相似度检索历史标书
- **📄 文档导出** - 一键导出Word和Markdown格式

### 技术亮点
- **🤖 LLM驱动** - 使用Ollama本地模型（qwen2:1.5b）
- **🗄️ 多数据库** - MySQL存储数据 + Milvus向量检索
- **🌐 RESTful API** - 完整的API接口
- **🎨 Web界面** - 简洁易用的测试平台

---

## 🚀 快速开始

### 前置要求
- Python 3.8+
- Docker & Docker Compose
- Ollama（可选，用于本地LLM）

### 1. 克隆项目
```bash
git clone <repository-url>
cd clawd
```

### 2. 安装依赖
```bash
pip install -r requirements.txt
```

### 3. 启动服务

#### 启动数据库服务（Docker）
```bash
docker-compose up -d
```

#### 启动Ollama（可选）
```bash
# 安装Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 拉取模型
ollama pull qwen2:1.5b

# 启动服务
ollama serve
```

#### 启动Web应用
```bash
python app_enhanced.py
```

### 4. 访问应用
打开浏览器访问：http://127.0.0.1:5000

---

## 📖 使用指南

### 生成标书

**API调用示例：**
```bash
curl -X POST http://127.0.0.1:5000/api/generate_bid \
  -H "Content-Type: application/json" \
  -d '{
    "project_name": "智慧城市综合管理平台",
    "project_description": "建设集交通管理、环境监测、公共安全等功能于一体的智慧城市平台",
    "requirements": [
      "系统集成度高",
      "实时数据处理",
      "AI智能分析"
    ]
  }'
```

**Python示例：**
```python
import requests

response = requests.post(
    'http://127.0.0.1:5000/api/generate_bid',
    json={
        'project_name': '智慧城市平台',
        'project_description': '...',
        'requirements': ['系统集成度高', '实时数据处理']
    }
)

bid_document = response.json()['bid_document']
print(bid_document)
```

### 质量评估

```python
response = requests.post(
    'http://127.0.0.1:5000/api/evaluate',
    json={
        'bid_content': bid_document,
        'requirements': ['系统集成度高', '实时数据处理']
    }
)

evaluation = response.json()['evaluation']
print(f"综合评分: {evaluation['overall_score']}分")
print(f"评级: {evaluation['overall_level']}")
```

### 导出文档

```python
response = requests.post(
    'http://127.0.0.1:5000/api/export',
    json={
        'bid_content': bid_document,
        'metadata': {
            'project_name': '智慧城市平台',
            'company': 'XX科技有限公司'
        },
        'format': 'word'
    }
)

file_path = response.json()['result']['word']
print(f"文档已导出: {file_path}")
```

### 多轮对话

```python
# 第一轮
response = requests.post(
    'http://127.0.0.1:5000/api/chat',
    json={
        'message': '请帮我完善技术方案部分'
    }
)
print(response.json()['response'])

# 第二轮（继续对话）
response = requests.post(
    'http://127.0.0.1:5000/api/chat',
    json={
        'message': '重点突出微服务架构优势'
    }
)
```

---

## 📁 项目结构

```
clawd/
├── app_enhanced.py           # Flask应用（增强版）
├── vector_store.py           # Milvus向量存储
├── bid_evaluator.py          # 标书质量评估
├── bid_exporter.py           # Word/Markdown导出
├── bid_conversation.py       # 多轮对话管理
├── bid_template.md           # 标书模板
│
├── tests/
│   ├── test_enhanced_features.py  # 功能测试
│   ├── test_bid_api.py            # API测试
│   ├── code_quality_check.py      # 代码质量检查
│   └── security_check.py          # 安全检查
│
├── docs/
│   ├── API_文档.md                # API文档
│   ├── CODE_QUALITY_REPORT.md     # 代码质量报告
│   └── PROJECT_SUMMARY.md         # 项目总结
│
├── docker-compose.yml         # Docker编排
├── create_tables.sql         # 数据库表结构
└── requirements.txt          # Python依赖
```

---

## 🔧 配置说明

### 数据库配置
```python
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,           # Docker映射端口
    'user': 'root',
    'password': 'tender123',
    'database': 'bid_system'
}
```

### Ollama配置
```python
OLLAMA_CONFIG = {
    'base_url': 'http://localhost:11434',
    'model': 'qwen2:1.5b'
}
```

### Milvus配置
```python
MILVUS_CONFIG = {
    'host': 'localhost',
    'port': '19530'
}
```

---

## 🧪 测试

### 运行所有测试
```bash
python test_enhanced_features.py
```

### 代码质量检查
```bash
python code_quality_check.py
```

### 安全检查
```bash
python security_check.py
```

---

## 📊 API文档

详细的API文档请参考：[API_文档.md](./API_文档.md)

### 主要端点

| 端点 | 方法 | 功能 |
|------|------|------|
| `/api/status` | GET | 系统状态检查 |
| `/api/generate_bid` | POST | 生成标书 |
| `/api/evaluate` | POST | 质量评估 |
| `/api/export` | POST | 导出文档 |
| `/api/chat` | POST | 多轮对话 |
| `/api/vector/search` | POST | 向量检索 |

---

## 🛠️ 开发指南

### 添加新功能
1. 在对应模块中实现功能
2. 在`app_enhanced.py`中添加API端点
3. 编写测试用例
4. 更新文档

### 代码规范
- 遵循PEP 8规范
- 使用类型提示
- 添加文档字符串
- 使用logging而非print

### 提交代码
```bash
# 格式化代码
black *.py

# 代码检查
pylint *.py

# 运行测试
python test_enhanced_features.py
```

---

## 🐛 常见问题

### Q: Ollama连接失败？
**A:** 确保Ollama服务正在运行：
```bash
ollama serve
```

### Q: 数据库连接失败？
**A:** 检查Docker容器状态：
```bash
docker-compose ps
docker-compose logs mysql
```

### Q: Word导出失败？
**A:** 安装python-docx：
```bash
pip install python-docx
```

### Q: 标书生成速度慢？
**A:** 考虑使用更快的模型或优化提示词：
```python
OLLAMA_CONFIG = {
    'model': 'qwen2:0.5b'  # 更快但精度略低
}
```

---

## 📈 性能优化建议

1. **使用更快的LLM模型**
   - `qwen2:0.5b` - 速度快，适合快速迭代
   - `qwen2:1.5b` - 平衡速度和质量
   - `qwen3:4b` - 高质量，适合生产

2. **启用缓存**
   ```python
   from functools import lru_cache

   @lru_cache(maxsize=100)
   def cached_query(prompt):
       return query_ollama(prompt)
   ```

3. **数据库连接池**
   ```python
   from mysql.connector import pooling

   db_pool = pooling.MySQLConnectionPool(
       pool_name="bid_pool",
       pool_size=5,
       **DB_CONFIG
   )
   ```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

1. Fork项目
2. 创建特性分支
3. 提交更改
4. 推送到分支
5. 创建Pull Request

---

## 📄 许可证

MIT License - 详见 [LICENSE](LICENSE) 文件

---

## 👥 维护者

- **Dev** - AI Assistant
- **陛下** - 项目Owner

---

## 🙏 致谢

- [Ollama](https://ollama.com) - 本地LLM运行环境
- [Flask](https://flask.palletsprojects.com/) - Web框架
- [Milvus](https://milvus.io/) - 向量数据库
- [python-docx](https://python-docx.readthedocs.io/) - Word文档生成

---

## 📞 联系方式

- 项目地址：[GitHub](https://github.com/your-repo)
- 问题反馈：[Issues](https://github.com/your-repo/issues)
- 邮箱：your-email@example.com

---

**最后更新：** 2026-01-31
**版本：** v1.0（增强版）
**状态：** ✅ 运行中

---

<p align="center">
  <b>⭐ 如果这个项目对你有帮助，请给个星标！</b>
</p>
