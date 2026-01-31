#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
标书向量存储模块
使用Milvus存储和检索标书相关内容
"""
import sys
import io

from pymilvus import connections, Collection, FieldSchema, CollectionSchema, DataType, utility
import numpy as np
from typing import List, Dict, Optional
import json

class TenderVectorStore:
    """标书向量存储"""

    def __init__(self, host='localhost', port='19530'):
        """初始化"""
        self.host = host
        self.port = port
        self.collection_name = 'tender_documents'
        self.dimension = 768  # 通用向量维度
        self._connect()

    def _connect(self):
        """连接Milvus"""
        if not connections.has_connection("default"):
            connections.connect(
                alias="default",
                host=self.host,
                port=self.port
            )

    def create_collection(self):
        """创建集合"""
        # 如果已存在则删除
        if utility.has_collection(self.collection_name):
            utility.drop_collection(self.collection_name)

        # 定义schema
        fields = [
            FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
            FieldSchema(name="doc_type", dtype=DataType.VARCHAR, max_length=50),
            FieldSchema(name="content", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="metadata", dtype=DataType.VARCHAR, max_length=65535),
            FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=self.dimension)
        ]

        schema = CollectionSchema(fields=fields, description="标书文档向量库")
        self.collection = Collection(
            name=self.collection_name,
            schema=schema
        )

        # 创建索引
        index_params = {
            "index_type": "IVF_FLAT",
            "metric_type": "IP",  # 内积
            "params": {"nlist": 128}
        }
        self.collection.create_index(field_name="embedding", index_params=index_params)

        print(f"✓ 创建集合: {self.collection_name}")

    def get_collection(self):
        """获取集合"""
        if not utility.has_collection(self.collection_name):
            self.create_collection()

        if not hasattr(self, 'collection') or self.collection is None:
            self.collection = Collection(self.collection_name)

        return self.collection

    def insert_document(self, doc_type: str, content: str, embedding: np.ndarray, metadata: Dict = None):
        """插入文档"""
        collection = self.get_collection()

        if metadata is None:
            metadata = {}

        data = [{
            "doc_type": doc_type,
            "content": content,
            "metadata": json.dumps(metadata, ensure_ascii=False),
            "embedding": embedding.tolist() if isinstance(embedding, np.ndarray) else embedding
        }]

        collection.insert(data)
        collection.flush()
        return True

    def search(self, query_embedding: np.ndarray, top_k: int = 5, doc_type: str = None):
        """搜索相似文档"""
        collection = self.get_collection()
        collection.load()

        # 构建搜索表达式
        expr = f"doc_type == '{doc_type}'" if doc_type else None

        results = collection.search(
            data=[query_embedding.tolist() if isinstance(query_embedding, np.ndarray) else query_embedding],
            anns_field="embedding",
            param={"metric_type": "IP", "params": {"nprobe": 10}},
            limit=top_k,
            expr=expr,
            output_fields=["doc_type", "content", "metadata"]
        )

        formatted_results = []
        for hit in results[0]:
            formatted_results.append({
                "content": hit.entity.get("content"),
                "doc_type": hit.entity.get("doc_type"),
                "metadata": json.loads(hit.entity.get("metadata", "{}")),
                "score": float(hit.score)
            })

        return formatted_results

    def insert_sample_data(self):
        """插入示例数据"""
        print("=== 插入示例数据 ===")

        # 示例标书片段
        sample_docs = [
            {
                "type": "technical_solution",
                "content": "采用微服务架构设计，系统分为用户层、应用层、服务层和数据层。使用Spring Cloud构建微服务框架，通过Nacos实现服务注册与发现。前端采用Vue.js框架，后端使用Java Spring Boot，数据库采用MySQL集群，Redis作为缓存。",
                "metadata": {"project": "智慧城市", "quality": "high"}
            },
            {
                "type": "team_structure",
                "content": "项目团队配备项目经理1名、系统架构师1名、高级开发工程师5名、测试工程师2名、UI设计师1名。项目经理具备PMP认证，10年以上项目管理经验。核心团队成员均具备5年以上相关领域经验。",
                "metadata": {"project": "政务系统", "quality": "high"}
            },
            {
                "type": "quality_assurance",
                "content": "建立完善的质量保障体系，包括代码审查、单元测试、集成测试、性能测试和安全测试。使用Jenkins进行持续集成，SonarQube进行代码质量分析。测试覆盖率达到85%以上，关键路径覆盖率达到100%。",
                "metadata": {"project": "金融系统", "quality": "high"}
            },
            {
                "type": "implementation_plan",
                "content": "项目分为五个阶段：需求调研（2周）、系统设计（3周）、开发实施（8周）、测试验收（3周）、上线部署（2周）。采用敏捷开发模式，每两周一个迭代，确保项目按计划推进。每周召开项目例会，及时解决风险和问题。",
                "metadata": {"project": "企业ERP", "quality": "medium"}
            },
            {
                "type": "after_sales",
                "content": "提供1年免费质保期，7×24小时技术支持热线。重大故障30分钟内响应，2小时内到达现场。提供3次免费现场培训和在线培训文档。建立专属服务群，配备客户经理和技术支持团队。",
                "metadata": {"project": "通用模板", "quality": "medium"}
            }
        ]

        # 使用随机向量（实际应使用embedding模型）
        for doc in sample_docs:
            embedding = np.random.rand(self.dimension).astype(np.float32)
            self.insert_document(
                doc_type=doc["type"],
                content=doc["content"],
                embedding=embedding,
                metadata=doc["metadata"]
            )
            print(f"✓ 插入: {doc['type']}")

        print(f"✓ 共插入 {len(sample_docs)} 条示例数据")

# 测试
if __name__ == '__main__':
    store = TenderVectorStore()
    store.create_collection()
    store.insert_sample_data()

    # 测试搜索
    query = np.random.rand(768).astype(np.float32)
    results = store.search(query, top_k=3)

    print("\n=== 搜索测试 ===")
    for r in results:
        print(f"[{r['doc_type']}] {r['content'][:50]}... (score: {r['score']:.3f})")
