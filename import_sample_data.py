#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
导入示例数据到MySQL数据库
"""
import mysql.connector
import json
import sys
from datetime import datetime

# 设置UTF-8输出
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3307,
    'user': 'root',
    'password': 'tender123',
    'database': 'bid_system'
}

# 示例员工数据
STAFF_DATA = [
    {
        "employee_id": "E001",
        "name": "张伟",
        "title": "技术总监",
        "department": "技术部",
        "education": "硕士",
        "specialization": "计算机科学与技术",
        "experience": 15,
        "phone": "13800001001",
        "email": "zhangwei@company.com",
        "skills": ["系统架构", "微服务", "云计算", "大数据", "AI技术"],
        "is_available": True,
        "remarks": "资深技术专家，主持过多个大型项目"
    },
    {
        "employee_id": "E002",
        "name": "李娜",
        "title": "项目经理",
        "department": "项目部",
        "education": "本科",
        "specialization": "软件工程",
        "experience": 10,
        "phone": "13800001002",
        "email": "lina@company.com",
        "skills": ["项目管理", "PMP认证", "需求分析", "风险控制"],
        "is_available": True,
        "remarks": "PMP认证项目经理"
    },
    {
        "employee_id": "E003",
        "name": "王强",
        "title": "高级工程师",
        "department": "研发部",
        "education": "硕士",
        "specialization": "人工智能",
        "experience": 8,
        "phone": "13800001003",
        "email": "wangqiang@company.com",
        "skills": ["Python", "机器学习", "深度学习", "NLP", "TensorFlow"],
        "is_available": True,
        "remarks": "AI领域专家"
    },
    {
        "employee_id": "E004",
        "name": "刘敏",
        "title": "UI/UX设计师",
        "department": "设计部",
        "education": "本科",
        "specialization": "视觉设计",
        "experience": 6,
        "phone": "13800001004",
        "email": "liumin@company.com",
        "skills": ["UI设计", "UX设计", "Figma", "Sketch", "用户体验"],
        "is_available": True,
        "remarks": "多次获得设计奖项"
    },
    {
        "employee_id": "E005",
        "name": "陈建国",
        "title": "质量经理",
        "department": "质量部",
        "education": "本科",
        "specialization": "质量管理",
        "experience": 12,
        "phone": "13800001005",
        "email": "chenjianguo@company.com",
        "skills": ["质量保证", "ISO9001", "测试管理", "流程优化"],
        "is_available": True,
        "remarks": "ISO9001内审员"
    },
    {
        "employee_id": "E006",
        "name": "赵晓丽",
        "title": "前端工程师",
        "department": "研发部",
        "education": "本科",
        "specialization": "软件工程",
        "experience": 5,
        "phone": "13800001006",
        "email": "zhaoxiaoli@company.com",
        "skills": ["React", "Vue", "TypeScript", "前端架构"],
        "is_available": True,
        "remarks": "前端技术栈全面"
    },
    {
        "employee_id": "E007",
        "name": "孙浩",
        "title": "后端工程师",
        "department": "研发部",
        "education": "硕士",
        "specialization": "计算机系统结构",
        "experience": 7,
        "phone": "13800001007",
        "email": "sunhao@company.com",
        "skills": ["Java", "Spring Boot", "微服务", "数据库优化"],
        "is_available": True,
        "remarks": "后端架构专家"
    },
    {
        "employee_id": "E008",
        "name": "周婷",
        "title": "测试工程师",
        "department": "质量部",
        "education": "本科",
        "specialization": "软件测试",
        "experience": 4,
        "phone": "13800001008",
        "email": "zhouting@company.com",
        "skills": ["自动化测试", "性能测试", "Selenium", "JMeter"],
        "is_available": True,
        "remarks": "测试经验丰富"
    },
    {
        "employee_id": "E009",
        "name": "吴磊",
        "title": "运维工程师",
        "department": "运维部",
        "education": "本科",
        "specialization": "网络工程",
        "experience": 6,
        "phone": "13800001009",
        "email": "wulei@company.com",
        "skills": ["Linux", "Docker", "Kubernetes", "CI/CD", "云运维"],
        "is_available": True,
        "remarks": "DevOps实践者"
    },
    {
        "employee_id": "E010",
        "name": "郑秀兰",
        "title": "商务经理",
        "department": "商务部",
        "education": "MBA",
        "specialization": "工商管理",
        "experience": 11,
        "phone": "13800001010",
        "email": "zhengxiulan@company.com",
        "skills": ["商务谈判", "合同管理", "客户关系", "市场分析"],
        "is_available": True,
        "remarks": "资深商务专家"
    },
    {
        "employee_id": "E011",
        "name": "马云龙",
        "title": "安全工程师",
        "department": "安全部",
        "education": "硕士",
        "specialization": "网络安全",
        "experience": 9,
        "phone": "13800001011",
        "email": "mayunlong@company.com",
        "skills": ["网络安全", "渗透测试", "安全加固", "等保认证"],
        "is_available": True,
        "remarks": "CISSP认证"
    },
    {
        "employee_id": "E012",
        "name": "黄小燕",
        "title": "数据分析师",
        "department": "数据部",
        "education": "硕士",
        "specialization": "统计学",
        "experience": 5,
        "phone": "13800001012",
        "email": "huangxiaoyan@company.com",
        "skills": ["数据分析", "Python", "SQL", "Tableau", "机器学习"],
        "is_available": True,
        "remarks": "数据驱动决策专家"
    }
]

# 示例产品数据
PRODUCTS_DATA = [
    {
        "product_code": "P001",
        "name": "智慧城市管理平台",
        "category": "智慧城市",
        "specifications": "B/S架构，支持微服务部署，高可用性设计",
        "description": "集成交通管理、环境监测、公共安全等功能的综合管理平台",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P002",
        "name": "AI智能客服系统",
        "category": "人工智能",
        "specifications": "基于NLP技术，支持多轮对话，知识库管理",
        "description": "智能客服机器人，7x24小时在线服务，自动应答常见问题",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P003",
        "name": "企业数据中台",
        "category": "大数据",
        "specifications": "支持PB级数据处理，实时计算，离线分析",
        "description": "统一数据管理平台，打破数据孤岛，实现数据价值最大化",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P004",
        "name": "物联网设备管理平台",
        "category": "物联网",
        "specifications": "支持百万级设备接入，MQTT协议，边缘计算",
        "description": "物联网设备统一管理、监控、运维平台",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P005",
        "name": "云原生应用平台",
        "category": "云计算",
        "specifications": "基于Kubernetes，支持多云管理，DevOps流水线",
        "description": "云原生应用全生命周期管理平台",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P006",
        "name": "视频监控分析系统",
        "category": "安防",
        "specifications": "支持AI识别，行为分析，人脸检测，车牌识别",
        "description": "智能视频监控分析系统，实时预警，事后追溯",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P007",
        "name": "电子政务办公系统",
        "category": "电子政务",
        "specifications": "符合国家电子政务标准，支持公文流转，审批流程",
        "description": "政府部门办公自动化系统，提高办公效率",
        "manufacturer": "本公司",
        "is_available": True
    },
    {
        "product_code": "P008",
        "name": "移动应用开发平台",
        "category": "移动开发",
        "specifications": "跨平台开发，支持iOS、Android、小程序",
        "description": "快速构建企业移动应用，统一管理，一键发布",
        "manufacturer": "本公司",
        "is_available": True
    }
]

# 示例资质数据
QUALIFICATIONS_DATA = [
    {
        "name": "信息系统集成及服务一级资质",
        "level": "一级",
        "issuer": "中国电子信息行业联合会",
        "certificate_no": "XZ20240001",
        "valid_until": "2026-12-31",
        "scope": "可独立承担计算机信息系统集成项目"
    },
    {
        "name": "CMMI 5级认证",
        "level": "5级",
        "issuer": "CMMI Institute",
        "certificate_no": "CMMI-ML5-2024",
        "valid_until": "2027-06-30",
        "scope": "软件能力成熟度最高级别认证"
    },
    {
        "name": "ISO9001质量管理体系认证",
        "level": "认证",
        "issuer": "SGS",
        "certificate_no": "ISO9001-2024-Q",
        "valid_until": "2027-03-15",
        "scope": "软件开发、系统集成质量管理"
    },
    {
        "name": "ISO27001信息安全管理体系",
        "level": "认证",
        "issuer": "DNV",
        "certificate_no": "ISO27001-2024-IS",
        "valid_until": "2027-05-20",
        "scope": "信息安全管理"
    },
    {
        "name": "高新技术企业证书",
        "level": "国家级",
        "issuer": "科学技术部",
        "certificate_no": "GR202411000000",
        "valid_until": "2027-11-30",
        "scope": "拥有自主知识产权的高新技术企业"
    },
    {
        "name": "涉密信息系统集成资质",
        "level": "乙级",
        "issuer": "国家保密局",
        "certificate_no": "BM2024-Y002",
        "valid_until": "2026-09-30",
        "scope": "涉密信息系统集成业务"
    },
    {
        "name": "安防工程企业设计施工维护能力证书",
        "level": "一级",
        "issuer": "中国安全防范产品行业协会",
        "certificate_no": "AF2024-1-0001",
        "valid_until": "2026-08-15",
        "scope": "安防工程设计、施工、维护"
    },
    {
        "name": "电子与智能化工程专业承包",
        "level": "一级",
        "issuer": "住房和城乡建设部",
        "certificate_no": "D1320240001",
        "valid_until": "2028-12-31",
        "scope": "电子与智能化工程施工"
    },
    {
        "name": "信息安全服务资质（安全工程类）",
        "level": "一级",
        "issuer": "中国网络安全审查技术与认证中心",
        "certificate_no": "CCRC-2024-1-0001",
        "valid_until": "2027-04-30",
        "scope": "信息安全服务"
    },
    {
        "name": "ITSS信息技术服务标准",
        "level": "一级",
        "issuer": "中国电子工业标准化技术协会",
        "certificate_no": "ITSS-2024-1-0001",
        "valid_until": "2027-07-31",
        "scope": "信息技术运行维护服务"
    }
]

def insert_staff(cursor, data):
    """插入员工数据"""
    sql = """
        INSERT INTO staff (employee_id, name, title, department, education,
                         specialization, experience, phone, email, skills,
                         is_available, remarks)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        title = VALUES(title),
        department = VALUES(department),
        education = VALUES(education),
        specialization = VALUES(specialization),
        experience = VALUES(experience),
        phone = VALUES(phone),
        email = VALUES(email),
        skills = VALUES(skills),
        is_available = VALUES(is_available),
        remarks = VALUES(remarks)
    """
    for item in data:
        cursor.execute(sql, (
            item['employee_id'],
            item['name'],
            item['title'],
            item['department'],
            item['education'],
            item['specialization'],
            item['experience'],
            item.get('phone'),
            item.get('email'),
            json.dumps(item['skills'], ensure_ascii=False),
            item.get('is_available', True),
            item.get('remarks')
        ))

def insert_products(cursor, data):
    """插入产品数据"""
    sql = """
        INSERT INTO products (product_code, name, category, specifications,
                            description, manufacturer, is_available)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        name = VALUES(name),
        category = VALUES(category),
        specifications = VALUES(specifications),
        description = VALUES(description),
        manufacturer = VALUES(manufacturer),
        is_available = VALUES(is_available)
    """
    for item in data:
        cursor.execute(sql, (
            item['product_code'],
            item['name'],
            item['category'],
            item.get('specifications'),
            item.get('description'),
            item.get('manufacturer'),
            item.get('is_available', True)
        ))

def insert_qualifications(cursor, data):
    """插入资质数据"""
    # 删除旧表（如果存在）并创建新表
    cursor.execute("DROP TABLE IF EXISTS qualifications")
    cursor.execute("""
        CREATE TABLE qualifications (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            level VARCHAR(50),
            issuer VARCHAR(200),
            certificate_no VARCHAR(100) UNIQUE,
            valid_until DATE,
            scope TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_name (name),
            INDEX idx_level (level)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='资质表'
    """)

    sql = """
        INSERT INTO qualifications (name, level, issuer, certificate_no,
                                   valid_until, scope)
        VALUES (%s, %s, %s, %s, %s, %s)
        ON DUPLICATE KEY UPDATE
        level = VALUES(level),
        issuer = VALUES(issuer),
        valid_until = VALUES(valid_until),
        scope = VALUES(scope)
    """
    for item in data:
        cursor.execute(sql, (
            item['name'],
            item['level'],
            item['issuer'],
            item['certificate_no'],
            item['valid_until'],
            item.get('scope')
        ))

def main():
    """主函数"""
    print("=== 导入示例数据到MySQL ===\n")

    try:
        # 连接数据库
        print("正在连接数据库...")
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        print("✓ 数据库连接成功\n")

        # 插入员工数据
        print(f"正在插入员工数据（{len(STAFF_DATA)}条）...")
        insert_staff(cursor, STAFF_DATA)
        print("✓ 员工数据导入完成\n")

        # 插入产品数据
        print(f"正在插入产品数据（{len(PRODUCTS_DATA)}条）...")
        insert_products(cursor, PRODUCTS_DATA)
        print("✓ 产品数据导入完成\n")

        # 插入资质数据
        print(f"正在插入资质数据（{len(QUALIFICATIONS_DATA)}条）...")
        insert_qualifications(cursor, QUALIFICATIONS_DATA)
        print("✓ 资质数据导入完成\n")

        # 提交事务
        conn.commit()
        print("✓ 所有数据导入成功！\n")

        # 验证数据
        print("=== 数据验证 ===\n")

        cursor.execute("SELECT COUNT(*) FROM staff")
        staff_count = cursor.fetchone()[0]
        print(f"员工总数：{staff_count}")

        cursor.execute("SELECT COUNT(*) FROM products")
        product_count = cursor.fetchone()[0]
        print(f"产品总数：{product_count}")

        cursor.execute("SELECT COUNT(*) FROM qualifications")
        qual_count = cursor.fetchone()[0]
        print(f"资质总数：{qual_count}\n")

        # 关闭连接
        cursor.close()
        conn.close()
        print("=== 导入完成 ===")

    except Exception as e:
        print(f"\n✗ 错误：{e}")
        if 'conn' in locals():
            conn.rollback()
            conn.close()

if __name__ == '__main__':
    main()
