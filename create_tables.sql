-- 创建staff表
CREATE TABLE IF NOT EXISTS staff (
    id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id VARCHAR(50) UNIQUE NOT NULL COMMENT '员工编号',
    name VARCHAR(50) NOT NULL COMMENT '姓名',
    title VARCHAR(50) COMMENT '职位',
    department VARCHAR(50) COMMENT '所属部门',
    education VARCHAR(50) COMMENT '学历',
    specialization VARCHAR(100) COMMENT '专业方向',
    experience INT DEFAULT 0 COMMENT '工作年限（年）',
    phone VARCHAR(20) COMMENT '联系电话',
    email VARCHAR(100) COMMENT '邮箱',
    skills JSON COMMENT '技能标签',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否可用',
    remarks TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_employee_id (employee_id),
    INDEX idx_title (title),
    INDEX idx_department (department),
    INDEX idx_is_available (is_available)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='员工表';

-- 创建products表
CREATE TABLE IF NOT EXISTS products (
    id INT AUTO_INCREMENT PRIMARY KEY,
    product_code VARCHAR(50) UNIQUE NOT NULL COMMENT '产品编码',
    name VARCHAR(200) NOT NULL COMMENT '产品名称',
    category VARCHAR(100) COMMENT '产品类别',
    specifications TEXT COMMENT '规格参数',
    description TEXT COMMENT '产品描述',
    manufacturer VARCHAR(200) COMMENT '制造商',
    is_available BOOLEAN DEFAULT TRUE COMMENT '是否可用',
    remarks TEXT COMMENT '备注',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_product_code (product_code),
    INDEX idx_category (category)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='产品表';

-- 查看所有表
SHOW TABLES;
