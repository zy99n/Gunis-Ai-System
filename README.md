# 企业智能协同平台 (Gunis-Ai-System)

> 基于 AI 驱动的企业级智能协同平台，提供组织管理、AI 模型管理、智能问数、数字员工等核心功能。

## 📋 项目简介

本项目是一个企业级智能协同平台，旨在通过人工智能技术提升企业内部协作效率和数据处理能力。平台包含完整的前后端分离架构，支持组织管理、AI 模型配置、自然语言查询、数字员工等核心业务场景。

## 🛠️ 技术栈

### 后端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Python | 3.10+ | 编程语言 |
| FastAPI | 0.104.1 | Web 框架 |
| Uvicorn | 0.24.0 | ASGI 服务器 |
| SQLAlchemy | 2.0.23 | ORM 框架（异步） |
| MySQL | 8.0+ | 关系型数据库 |
| Redis | 7.0+ | 缓存数据库 |
| PyJWT | 2.8.0 | JWT 认证 |
| Passlib | 1.7.4 | 密码加密 |
| Socket.IO | 5.10.0 | 实时通讯 |
| APScheduler | 3.10.4 | 定时任务 |

### 前端技术栈

| 技术 | 版本 | 说明 |
|------|------|------|
| Vue | 3.3.8 | 前端框架 |
| TypeScript | 5.2.2 | 类型脚本 |
| Element Plus | 2.4.2 | UI 组件库 |
| Vue Router | 4.2.5 | 路由管理 |
| Pinia | 2.1.7 | 状态管理 |
| Axios | 1.6.2 | HTTP 客户端 |
| ECharts | 5.4.3 | 数据可视化 |
| Vite | 5.0.2 | 构建工具 |

## 📁 项目结构

```
├── backend/                    # 后端代码
│   ├── apps/                   # 业务模块
│   │   ├── admin/              # 系统管理（敏感词、审计日志）
│   │   ├── auth/               # 用户认证（登录、注册）
│   │   ├── data/               # 数据采集（爬虫、ETL）
│   │   ├── employee/           # 数字员工管理
│   │   ├── im/                 # 即时通讯
│   │   ├── model/              # AI 模型管理
│   │   ├── nl2sql/             # 智能问数（NL2SQL）
│   │   ├── organization/       # 组织管理（部门、用户）
│   │   └── skill/              # AI 技能管理
│   ├── common/                 # 公共模块
│   │   ├── config/             # 配置管理
│   │   ├── database/           # 数据库会话
│   │   ├── middleware/         # 中间件（JWT、CORS、日志）
│   │   └── security/           # 安全工具（JWT、密码）
│   ├── core/                   # 核心模块
│   │   ├── base_model.py       # 基础模型
│   │   ├── base_service.py     # 基础服务
│   │   └── dependency.py       # 依赖注入
│   ├── main.py                 # 应用入口
│   └── requirements.txt        # 依赖清单
├── frontend/                   # 前端代码
│   ├── src/
│   │   ├── api/                # API 请求层
│   │   ├── layouts/            # 布局组件
│   │   ├── modules/            # 业务模块页面
│   │   ├── router/             # 路由配置
│   │   ├── store/              # Pinia 状态管理
│   │   ├── styles/             # 全局样式
│   │   ├── utils/              # 工具函数
│   │   ├── App.vue             # 根组件
│   │   └── main.ts             # 入口文件
│   ├── index.html              # HTML 模板
│   ├── package.json            # 依赖配置
│   ├── tsconfig.json           # TypeScript 配置
│   └── vite.config.ts          # Vite 配置
├── database/                   # 数据库初始化
│   └── init.sql                # 数据库初始化脚本
└── README.md                   # 项目说明文档
```

## 🔌 功能模块

### 核心模块

| 模块 | 功能描述 |
|------|----------|
| **组织管理** | 部门树形结构管理、用户管理、用户-部门关联 |
| **AI 模型管理** | 模型配置、测试连通性、设置默认模型 |
| **智能问数** | 自然语言转 SQL、查询执行、历史记录、收藏 |
| **AI 技能管理** | 技能创建、AI 生成技能、技能测试、启用/禁用 |

### 辅助模块

| 模块 | 功能描述 |
|------|----------|
| **系统管理** | 敏感词管理、操作审计日志 |
| **数字员工** | 数字员工 CRUD、状态管理、聊天入口 |
| **数据采集** | 爬虫任务管理、ETL 流水线配置 |
| **即时通讯** | 消息列表、实时聊天、未读消息提醒 |

## 🚀 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- MySQL 8.0+
- Redis 7.0+

### 1. 克隆项目

```bash
git clone https://github.com/zy99n/Gunis-Ai-System.git
cd Gunis-Ai-System
```

### 2. 后端部署

#### 安装依赖

```bash
cd backend
pip install -r requirements.txt
```

#### 数据库配置

修改 `backend/common/config/settings.py` 中的数据库连接配置：

```python
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/database_name"
REDIS_URL = "redis://localhost:6379/0"
```

#### 初始化数据库

```bash
mysql -u username -p database_name < database/init.sql
```

#### 启动后端服务

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

后端服务启动后访问：http://localhost:8000

### 3. 前端部署

#### 安装依赖

```bash
cd frontend
npm install
```

#### 启动开发服务器

```bash
npm run dev
```

前端服务启动后访问：http://localhost:3000

#### 构建生产版本

```bash
npm run build
```

## 🔐 API 认证

本项目使用 JWT 认证机制：

1. 登录获取 Token：`POST /api/auth/login`
2. 在请求头中携带 Token：`Authorization: Bearer <token>`
3. 后端中间件自动验证 Token 有效性

## 📡 API 接口

### 认证接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/auth/login` | 用户登录 |
| POST | `/api/auth/register` | 用户注册 |
| GET | `/api/auth/me` | 获取当前用户信息 |

### 组织管理接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/organization/departments/tree` | 获取部门树形结构 |
| GET | `/api/organization/departments` | 获取部门列表 |
| POST | `/api/organization/departments` | 创建部门 |
| PUT | `/api/organization/departments/{id}` | 更新部门 |
| DELETE | `/api/organization/departments/{id}` | 删除部门 |

### AI 模型管理接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/model/models` | 获取模型列表 |
| POST | `/api/model/models` | 创建模型 |
| PUT | `/api/model/models/{id}/set-default` | 设置默认模型 |
| POST | `/api/model/models/{id}/test` | 测试模型连通性 |

### 智能问数接口

| 方法 | 路径 | 描述 |
|------|------|------|
| POST | `/api/nl2sql/query` | 执行自然语言查询 |
| GET | `/api/nl2sql/history` | 获取查询历史 |
| POST | `/api/nl2sql/favorites` | 添加收藏 |

### AI 技能管理接口

| 方法 | 路径 | 描述 |
|------|------|------|
| GET | `/api/skill/skills` | 获取技能列表 |
| POST | `/api/skill/skills` | 创建技能 |
| POST | `/api/skill/skills/{id}/generate` | AI 生成技能 |
| POST | `/api/skill/skills/{id}/test` | 测试技能 |

## 🤝 团队协作

### Git 工作流

1. 从 `main` 分支创建功能分支：`git checkout -b feature/xxx`
2. 完成开发后提交：`git add . && git commit -m "feat: xxx"`
3. 推送分支：`git push origin feature/xxx`
4. 创建 Pull Request 进行代码审查
5. 审查通过后合并到 `main` 分支

### 代码规范

- **后端**: 遵循 PEP 8 规范，使用 Type Hints
- **前端**: 遵循 ESLint 规则，使用 TypeScript
- **提交信息**: 使用 Conventional Commits 格式

## 📝 开发计划

| 阶段 | 时间 | 任务 |
|------|------|------|
| Day 1 | 第1天 | 项目初始化、用户认证模块、基础配置 |
| Day 2 | 第2天 | 组织管理、AI 模型管理、NL2SQL、AI 技能管理 |
| Day 3 | 第3天 | 数字员工、数据采集、即时通讯、系统管理 |
| Day 4 | 第4天 | 联调测试、文档完善、项目部署 |

## 📄 许可证

本项目仅供学习和研究使用。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- GitHub: [https://github.com/zy99n/Gunis-Ai-System](https://github.com/zy99n/Gunis-Ai-System)