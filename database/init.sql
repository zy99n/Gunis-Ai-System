-- =========================================
-- 企业智能协同平台 - 数据库初始化脚本
-- 数据库: MySQL 8.0+
-- 创建时间: 2024
-- =========================================

-- 创建数据库
CREATE DATABASE IF NOT EXISTS enterprise_collab CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE enterprise_collab;

-- =========================================
-- 1. 用户表
-- =========================================
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE COMMENT '用户名',
    email VARCHAR(100) NOT NULL UNIQUE COMMENT '邮箱',
    password_hash VARCHAR(255) NOT NULL COMMENT '密码哈希',
    nickname VARCHAR(50) COMMENT '昵称',
    avatar VARCHAR(255) COMMENT '头像URL',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否激活',
    is_admin TINYINT(1) DEFAULT 0 COMMENT '是否管理员',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户表';

-- =========================================
-- 2. 部门表
-- =========================================
CREATE TABLE IF NOT EXISTS departments (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '部门名称',
    parent_id INT DEFAULT NULL COMMENT '父部门ID',
    sort_order INT DEFAULT 0 COMMENT '排序',
    description TEXT COMMENT '部门描述',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (parent_id) REFERENCES departments(id) ON DELETE SET NULL,
    INDEX idx_parent_id (parent_id),
    INDEX idx_sort_order (sort_order),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='部门表';

-- =========================================
-- 3. 用户-部门关联表
-- =========================================
CREATE TABLE IF NOT EXISTS user_department (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL COMMENT '用户ID',
    department_id INT NOT NULL COMMENT '部门ID',
    is_primary TINYINT(1) DEFAULT 1 COMMENT '是否为主部门',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_user_dept (user_id, department_id),
    INDEX idx_user_id (user_id),
    INDEX idx_dept_id (department_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='用户部门关联表';

-- =========================================
-- 4. AI模型表
-- =========================================
CREATE TABLE IF NOT EXISTS ai_models (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '模型名称',
    model_type VARCHAR(50) NOT NULL COMMENT '模型类型: openai, anthropic, google, baidu, aliyun, custom',
    api_base VARCHAR(500) COMMENT 'API基础地址',
    api_key VARCHAR(500) NOT NULL COMMENT 'API密钥',
    model_name VARCHAR(100) NOT NULL COMMENT '模型名称',
    temperature DECIMAL(3,2) DEFAULT 0.7 COMMENT '温度参数',
    max_tokens INT DEFAULT 2000 COMMENT '最大token数',
    timeout INT DEFAULT 30 COMMENT '超时时间(秒)',
    is_default TINYINT(1) DEFAULT 0 COMMENT '是否默认模型',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    description TEXT COMMENT '描述',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_model_type (model_type),
    INDEX idx_is_default (is_default),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI模型配置表';

-- =========================================
-- 5. AI技能表
-- =========================================
CREATE TABLE IF NOT EXISTS ai_skills (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '技能名称',
    code VARCHAR(50) NOT NULL UNIQUE COMMENT '技能编码',
    description TEXT COMMENT '技能描述',
    prompt_template TEXT NOT NULL COMMENT '提示词模板',
    model_id INT COMMENT '关联模型ID',
    parameters JSON COMMENT '参数配置JSON',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    category VARCHAR(50) COMMENT '分类',
    icon VARCHAR(100) COMMENT '图标',
    sort_order INT DEFAULT 0 COMMENT '排序',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_model_id (model_id),
    INDEX idx_category (category),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='AI技能表';

-- =========================================
-- 6. 数字员工表
-- =========================================
CREATE TABLE IF NOT EXISTS digital_employees (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '员工名称',
    avatar VARCHAR(255) COMMENT '头像',
    description TEXT COMMENT '描述',
    model_id INT COMMENT '默认模型ID',
    system_prompt TEXT COMMENT '系统提示词',
    greeting TEXT COMMENT '欢迎语',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_by INT COMMENT '创建人ID',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_model_id (model_id),
    INDEX idx_created_by (created_by),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数字员工表';

-- =========================================
-- 7. 数字员工-技能关联表
-- =========================================
CREATE TABLE IF NOT EXISTS employee_skill (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL COMMENT '数字员工ID',
    skill_id INT NOT NULL COMMENT '技能ID',
    sort_order INT DEFAULT 0 COMMENT '排序',
    config JSON COMMENT '个性化配置',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    UNIQUE KEY uk_employee_skill (employee_id, skill_id),
    INDEX idx_employee_id (employee_id),
    INDEX idx_skill_id (skill_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数字员工技能关联表';

-- =========================================
-- 8. NL2SQL查询历史表
-- =========================================
CREATE TABLE IF NOT EXISTS nl2sql_queries (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL COMMENT '用户ID',
    natural_language TEXT NOT NULL COMMENT '自然语言查询',
    generated_sql TEXT COMMENT '生成的SQL',
    execution_result JSON COMMENT '执行结果',
    is_success TINYINT(1) COMMENT '是否执行成功',
    error_message TEXT COMMENT '错误信息',
    execution_time_ms INT COMMENT '执行耗时(毫秒)',
    is_favorite TINYINT(1) DEFAULT 0 COMMENT '是否收藏',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_is_favorite (is_favorite),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='NL2SQL查询历史表';

-- =========================================
-- 9. 数据采集-爬虫任务表
-- =========================================
CREATE TABLE IF NOT EXISTS crawler_tasks (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '任务名称',
    url VARCHAR(1000) NOT NULL COMMENT '目标URL',
    crawler_type VARCHAR(50) NOT NULL COMMENT '爬虫类型: static, dynamic, api',
    selectors JSON COMMENT '选择器配置',
    headers JSON COMMENT '请求头',
    interval_seconds INT DEFAULT 3600 COMMENT '执行间隔(秒)',
    max_retries INT DEFAULT 3 COMMENT '最大重试次数',
    timeout INT DEFAULT 30 COMMENT '超时时间(秒)',
    enabled TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    last_run_at DATETIME COMMENT '上次运行时间',
    next_run_at DATETIME COMMENT '下次运行时间',
    created_by INT COMMENT '创建人ID',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_enabled (enabled),
    INDEX idx_next_run_at (next_run_at),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='爬虫任务表';

-- =========================================
-- 10. ETL流水线表
-- =========================================
CREATE TABLE IF NOT EXISTS etl_pipelines (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '流水线名称',
    description TEXT COMMENT '描述',
    source_config JSON NOT NULL COMMENT '数据源配置',
    transform_config JSON COMMENT '转换配置',
    sink_config JSON NOT NULL COMMENT '目标配置',
    schedule_cron VARCHAR(100) COMMENT '定时表达式',
    enabled TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_by INT COMMENT '创建人ID',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_enabled (enabled),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='ETL流水线表';

-- =========================================
-- 11. 即时通讯-会话表
-- =========================================
CREATE TABLE IF NOT EXISTS conversations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    type VARCHAR(20) NOT NULL COMMENT '会话类型: single, group',
    name VARCHAR(100) COMMENT '会话名称',
    avatar VARCHAR(255) COMMENT '会话头像',
    creator_id INT NOT NULL COMMENT '创建人ID',
    last_message_at DATETIME COMMENT '最后消息时间',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type),
    INDEX idx_creator_id (creator_id),
    INDEX idx_last_message_at (last_message_at),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会话表';

-- =========================================
-- 12. 即时通讯-会话成员表
-- =========================================
CREATE TABLE IF NOT EXISTS conversation_members (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL COMMENT '会话ID',
    user_id INT NOT NULL COMMENT '用户ID',
    last_read_message_id INT COMMENT '最后已读消息ID',
    unread_count INT DEFAULT 0 COMMENT '未读消息数',
    joined_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '加入时间',
    UNIQUE KEY uk_conv_user (conversation_id, user_id),
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_user_id (user_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='会话成员表';

-- =========================================
-- 13. 即时通讯-消息表
-- =========================================
CREATE TABLE IF NOT EXISTS messages (
    id INT PRIMARY KEY AUTO_INCREMENT,
    conversation_id INT NOT NULL COMMENT '会话ID',
    sender_id INT NOT NULL COMMENT '发送人ID',
    content TEXT NOT NULL COMMENT '消息内容',
    message_type VARCHAR(20) DEFAULT 'text' COMMENT '消息类型: text, image, file, emoji',
    is_read TINYINT(1) DEFAULT 0 COMMENT '是否已读',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_conversation_id (conversation_id),
    INDEX idx_sender_id (sender_id),
    INDEX idx_is_read (is_read),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='消息表';

-- =========================================
-- 14. 敏感词表
-- =========================================
CREATE TABLE IF NOT EXISTS sensitive_words (
    id INT PRIMARY KEY AUTO_INCREMENT,
    word VARCHAR(100) NOT NULL UNIQUE COMMENT '敏感词',
    category VARCHAR(50) COMMENT '分类',
    replacement VARCHAR(50) DEFAULT '*' COMMENT '替换字符',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_word (word),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='敏感词表';

-- =========================================
-- 15. 审计日志表
-- =========================================
CREATE TABLE IF NOT EXISTS audit_logs (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT COMMENT '用户ID',
    username VARCHAR(50) COMMENT '用户名',
    action VARCHAR(100) NOT NULL COMMENT '操作',
    module VARCHAR(50) COMMENT '模块',
    resource_type VARCHAR(50) COMMENT '资源类型',
    resource_id INT COMMENT '资源ID',
    description TEXT COMMENT '描述',
    request_ip VARCHAR(50) COMMENT '请求IP',
    user_agent TEXT COMMENT '用户代理',
    status VARCHAR(20) COMMENT '状态: success, fail',
    error_message TEXT COMMENT '错误信息',
    execution_time_ms INT COMMENT '执行耗时',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_module (module),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='审计日志表';

-- =========================================
-- 16. 数据源表
-- =========================================
CREATE TABLE IF NOT EXISTS data_sources (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL COMMENT '数据源名称',
    type VARCHAR(50) NOT NULL COMMENT '数据源类型: mysql, postgresql, sqlite, oracle, sqlserver',
    connection_config JSON NOT NULL COMMENT '连接配置JSON',
    is_active TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    description TEXT COMMENT '描述',
    created_by INT COMMENT '创建人ID',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    INDEX idx_type (type),
    INDEX idx_is_active (is_active),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据源表';

-- =========================================
-- 17. 数据表元信息表
-- =========================================
CREATE TABLE IF NOT EXISTS data_tables (
    id INT PRIMARY KEY AUTO_INCREMENT,
    data_source_id INT NOT NULL COMMENT '数据源ID',
    table_name VARCHAR(100) NOT NULL COMMENT '表名',
    display_name VARCHAR(100) COMMENT '显示名称',
    description TEXT COMMENT '描述',
    columns_json JSON NOT NULL COMMENT '列定义JSON',
    is_enabled TINYINT(1) DEFAULT 1 COMMENT '是否启用',
    is_deleted TINYINT(1) DEFAULT 0 COMMENT '是否删除',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    FOREIGN KEY (data_source_id) REFERENCES data_sources(id) ON DELETE CASCADE,
    INDEX idx_data_source_id (data_source_id),
    INDEX idx_table_name (table_name),
    INDEX idx_is_enabled (is_enabled),
    INDEX idx_is_deleted (is_deleted)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数据表元信息表';

-- =========================================
-- 18. 数字员工对话记录表
-- =========================================
CREATE TABLE IF NOT EXISTS employee_chat_history (
    id INT PRIMARY KEY AUTO_INCREMENT,
    employee_id INT NOT NULL COMMENT '数字员工ID',
    user_id INT NOT NULL COMMENT '用户ID',
    session_id VARCHAR(100) NOT NULL COMMENT '会话ID',
    role VARCHAR(20) NOT NULL COMMENT '角色: user, assistant',
    content TEXT NOT NULL COMMENT '内容',
    tokens_used INT COMMENT '使用的token数',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    INDEX idx_employee_id (employee_id),
    INDEX idx_user_id (user_id),
    INDEX idx_session_id (session_id),
    INDEX idx_created_at (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci COMMENT='数字员工对话记录表';

-- =========================================
-- 初始化数据（支持重复执行）
-- =========================================

SET FOREIGN_KEY_CHECKS = 0;

-- 清理已存在的初始化数据
DELETE FROM user_department WHERE user_id = 1;
DELETE FROM departments WHERE parent_id IS NULL AND name = '总公司';
DELETE FROM ai_models WHERE name = 'GPT-3.5-Turbo';
DELETE FROM sensitive_words WHERE word IN ('违禁词', '敏感词');
DELETE FROM users WHERE username = 'admin';

SET FOREIGN_KEY_CHECKS = 1;

-- 插入超级管理员用户
-- 密码: admin123 哈希值由bcrypt生成
INSERT INTO users (username, email, password_hash, nickname, is_active, is_admin) VALUES 
('admin', 'admin@enterprise.com', '$2a$10$N.zmdr9k7uOCQb376NoUnuTJ8iAt6Z5EHsM8lE9lBOsl7iAt6zBXW', '超级管理员', 1, 1);

-- 插入默认部门
INSERT INTO departments (name, parent_id, sort_order) VALUES 
('总公司', NULL, 1),
('技术部', 1, 2),
('产品部', 1, 3),
('运营部', 1, 4),
('市场部', 1, 5);

-- 关联管理员到总公司
INSERT INTO user_department (user_id, department_id, is_primary) VALUES (1, 1, 1);

-- 插入默认AI模型
INSERT INTO ai_models (name, model_type, api_base, api_key, model_name, temperature, max_tokens, is_default, is_active, description) VALUES
('GPT-3.5-Turbo', 'openai', 'https://api.openai.com/v1', 'your-api-key', 'gpt-3.5-turbo', 0.7, 2000, 1, 1, 'OpenAI GPT-3.5 Turbo模型');

-- 插入默认敏感词示例
INSERT INTO sensitive_words (word, category, is_active) VALUES
('违禁词', '政治', 1),
('敏感词', '其他', 1);

-- 创建索引优化查询性能
-- 复合索引示例
CREATE INDEX idx_users_active_deleted ON users(is_active, is_deleted);
CREATE INDEX idx_departments_parent_deleted ON departments(parent_id, is_deleted);
CREATE INDEX idx_ai_models_active_default ON ai_models(is_active, is_default);