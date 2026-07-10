# 第二天编码计划 - 企业智能协同平台

## 📅 日期：Day 2
## 🎯 目标：完成核心模块（组织管理、模型管理、NL2SQL、技能管理）的前后端开发

---

## 📋 当前项目状态（Day 1已完成）

| 模块 | 状态 | 说明 |
|------|------|------|
| 认证模块 | ✅ | 注册/登录/JWT认证 |
| 前端框架 | ✅ | Vue3 + Element Plus + Router + Pinia |
| 后端框架 | ✅ | FastAPI + SQLAlchemy + MySQL |
| 数据库 | ✅ | init.sql已包含所有18张表结构 |

---

## 📊 单人开发优先级排序

| 优先级 | 模块 | 后端文件 | 前端文件 | 估算时间 |
|--------|------|----------|----------|----------|
| P0 | 组织管理 | organization/ | organization/ | 3小时 |
| P1 | AI模型管理 | model/ | model/ | 2小时 |
| P2 | NL2SQL智能问数 | nl2sql/ | nl2sql/ | 2.5小时 |
| P3 | AI技能管理 | skill/ | skill/ | 2小时 |
| P4 | 系统管理 | admin/ | admin/ | 1.5小时 |
| P5 | 数字员工 | employee/ | employee/ | 1.5小时 |
| P6 | 数据采集 | data/ | data/ | 1.5小时 |
| P7 | 即时通讯 | im/ | im/ | 2小时 |

> **说明**：单人开发建议优先完成P0-P3模块（核心功能），P4-P7模块可在Day 3继续完成。

---

## 📝 详细编码计划

---

### 模块1：组织管理（P0）

**后端 - `backend/apps/organization/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 部门模型、用户-部门关联 | Department继承BaseModel，使用现有departments表 |
| `schemas.py` | Pydantic验证 | DepartmentCreate, DepartmentUpdate, UserDepartmentCreate |
| `service.py` | 业务逻辑 | 部门CRUD、树形结构查询、用户-部门关联管理、移动部门 |
| `api.py` | API路由 | GET /departments/tree, POST/GET/PUT/DELETE /departments, PUT /departments/{id}/move, GET/POST/PUT/DELETE /users |

**前端 - `frontend/src/modules/organization/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/DepartmentManage.vue` | 部门管理页面 | 树形表格展示(el-tree)、新增/编辑/删除弹窗、拖拽排序(Sortable.js) |
| `pages/UserManage.vue` | 用户管理页面 | 表格列表(el-table)、搜索、分页(el-pagination)、新增/编辑/删除弹窗 |

**路由配置**:
```
/organization/department → DepartmentManage
/organization/user → UserManage
```

---

### 模块2：AI模型管理（P1）

**后端 - `backend/apps/model/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | AI模型配置 | AiModel继承BaseModel，使用现有ai_models表 |
| `schemas.py` | Pydantic验证 | AiModelCreate, AiModelUpdate, TestResult |
| `service.py` | 业务逻辑 | 模型CRUD、设置默认模型、测试连通性 |
| `api.py` | API路由 | GET/POST/PUT/DELETE /models, PUT /models/{id}/default, POST /models/{id}/test |

**前端 - `frontend/src/modules/model/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/ModelList.vue` | 模型列表页面 | 表格展示、搜索、测试连通性按钮、设为默认按钮 |
| `components/ModelEdit.vue` | 模型编辑弹窗 | 表单验证、API Key加密显示(***), model_type下拉选择 |

**路由配置**:
```
/model/list → ModelList
```

---

### 模块3：NL2SQL智能问数（P2）

**后端 - `backend/apps/nl2sql/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 查询历史 | QueryHistory继承BaseModel，使用nl2sql_queries表 |
| `schemas.py` | Pydantic验证 | QueryRequest, QueryResponse, HistoryResponse |
| `service.py` | 业务逻辑 | NL2SQL转换(模拟)、执行SQL、保存历史、收藏管理、导出Excel |
| `api.py` | API路由 | POST /query, GET /history, POST /history/{id}/favorite, GET /history/{id}/export/excel |

**前端 - `frontend/src/modules/nl2sql/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/QueryPanel.vue` | 查询面板主页面 | 查询输入框、结果表格/图表切换、历史列表侧边栏 |
| `components/QueryInput.vue` | 查询输入组件 | 自然语言输入、智能提示、发送按钮 |
| `components/ResultTable.vue` | 结果表格组件 | 动态列渲染、分页 |
| `components/ResultChart.vue` | 结果图表组件 | ECharts绑定、图表类型切换(柱状图/折线图/饼图) |

**路由配置**:
```
/nl2sql/query → QueryPanel
```

---

### 模块4：AI技能管理（P3）

**后端 - `backend/apps/skill/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 技能模型 | AiSkill继承BaseModel，使用ai_skills表 |
| `schemas.py` | Pydantic验证 | SkillCreate, SkillUpdate, SkillGenerateRequest |
| `service.py` | 业务逻辑 | 技能CRUD、AI辅助生成代码、技能测试、启用/禁用切换 |
| `api.py` | API路由 | GET/POST/PUT/DELETE /skills, POST /skills/ai-generate, POST /skills/{id}/test, PUT /skills/{id}/toggle |

**前端 - `frontend/src/modules/skill/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/SkillList.vue` | 技能列表页面 | 表格展示、搜索、新增/编辑、启用状态切换 |
| `components/SkillEdit.vue` | 技能编辑表单 | 代码编辑器(textarea)、参数配置(JSON)、AI辅助生成按钮 |

**路由配置**:
```
/skill/list → SkillList
```

---

### 模块5：系统管理（P4）

**后端 - `backend/apps/admin/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 敏感词、审计日志 | SensitiveWord继承BaseModel，AuditLog继承BaseModel |
| `schemas.py` | Pydantic验证 | SensitiveWordCreate, AuditLogQuery |
| `service.py` | 业务逻辑 | 敏感词CRUD、日志查询、敏感词过滤、审计日志记录 |
| `api.py` | API路由 | GET/POST/DELETE /sensitive-words, GET /audit-logs, GET /audit-logs/export |

**前端 - `frontend/src/modules/admin/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/SensitiveWords.vue` | 敏感词管理 | 表格展示、新增/删除、级别选择(block/audit) |
| `pages/AuditLogs.vue` | 审计日志 | 表格展示、搜索、时间范围筛选、导出按钮 |

**路由配置**:
```
/admin/sensitive → SensitiveWords
/admin/audit → AuditLogs
```

---

### 模块6：数字员工（P5）

**后端 - `backend/apps/employee/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 数字员工、技能绑定 | DigitalEmployee继承BaseModel，EmployeeSkill关联表 |
| `schemas.py` | Pydantic验证 | EmployeeCreate, EmployeeUpdate |
| `service.py` | 业务逻辑 | 员工CRUD、模型绑定、技能绑定、启用/禁用切换 |
| `api.py` | API路由 | GET/POST/PUT/DELETE /employees, PUT /employees/{id}/toggle |

**前端 - `frontend/src/modules/employee/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/EmployeeList.vue` | 员工列表页面 | 表格展示、搜索、新增/编辑、状态切换 |
| `components/EmployeeEdit.vue` | 员工编辑表单 | 模型选择器(el-select)、技能多选、系统提示词编辑、欢迎语编辑 |

**路由配置**:
```
/employee/list → EmployeeList
```

---

### 模块7：数据采集（P6）

**后端 - `backend/apps/data/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 爬虫任务、ETL流水线 | CrawlerTask, EtlPipeline继承BaseModel |
| `schemas.py` | Pydantic验证 | CrawlerTaskCreate, EtlPipelineCreate |
| `service.py` | 业务逻辑 | 任务CRUD、调度配置(cron)、手动触发 |
| `api.py` | API路由 | GET/POST/PUT/DELETE /crawler-tasks, POST /crawler-tasks/{id}/run, GET/POST/PUT/DELETE /etl-pipelines |

**前端 - `frontend/src/modules/data/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/CrawlerList.vue` | 爬虫任务列表 | 表格展示、状态展示、手动触发按钮 |
| `components/CrawlerEdit.vue` | 爬虫配置表单 | URL输入、请求方法选择、Headers配置 |
| `pages/EtlPipeline.vue` | ETL流水线配置 | 流程图组件、节点配置 |

**路由配置**:
```
/data/crawler → CrawlerList
/data/etl → EtlPipeline
```

---

### 模块8：即时通讯（P7）

**后端 - `backend/apps/im/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `models.py` | 会话、消息、成员 | Conversation, Message, ConversationMember继承BaseModel |
| `schemas.py` | Pydantic验证 | MessageCreate, ConversationResponse |
| `service.py` | 业务逻辑 | 会话管理、消息存储、成员管理 |
| `socket_handler.py` | Socket.IO处理器 | 实时消息发送、广播、已读回执 |
| `api.py` | API路由 | GET /conversations, POST /conversations/private, POST /conversations/group, GET/POST /conversations/{id}/messages |

**前端 - `frontend/src/modules/im/`**

| 文件 | 功能 | 关键实现 |
|------|------|----------|
| `pages/ChatRoom.vue` | 聊天室主页面 | 会话列表 + 消息列表 + 输入框三栏布局 |
| `components/ConversationList.vue` | 会话列表 | 最近消息、未读计数 |
| `components/MessageList.vue` | 消息列表 | 气泡展示、滚动加载 |
| `components/MessageInput.vue` | 消息输入 | 文本输入、发送按钮 |

**路由配置**:
```
/im/chat → ChatRoom
```

---

## 🔧 公共依赖与工具

### 后端新增API模块注册（main.py）

```python
# 在 main.py 中注册所有新路由
from apps.organization.api import router as organization_router
from apps.model.api import router as model_router
from apps.nl2sql.api import router as nl2sql_router
from apps.skill.api import router as skill_router
from apps.employee.api import router as employee_router
from apps.data.api import router as data_router
from apps.admin.api import router as admin_router
from apps.im.api import router as im_router

app.include_router(organization_router, prefix="/api/organization", tags=["组织管理"])
app.include_router(model_router, prefix="/api/model", tags=["模型管理"])
app.include_router(nl2sql_router, prefix="/api/nl2sql", tags=["智能问数"])
app.include_router(skill_router, prefix="/api/skill", tags=["AI技能"])
app.include_router(employee_router, prefix="/api/employee", tags=["数字员工"])
app.include_router(data_router, prefix="/api/data", tags=["数据采集"])
app.include_router(admin_router, prefix="/api/admin", tags=["系统管理"])
app.include_router(im_router, prefix="/api/im", tags=["即时通讯"])
```

### 前端API层（src/api/）

| 文件 | 功能 |
|------|------|
| `organization.ts` | 组织管理API调用 |
| `model.ts` | 模型管理API调用 |
| `nl2sql.ts` | NL2SQL API调用 |
| `skill.ts` | 技能管理API调用 |
| `employee.ts` | 数字员工API调用 |
| `data.ts` | 数据采集API调用 |
| `admin.ts` | 系统管理API调用 |
| `im.ts` | 即时通讯API调用 |

---

## 📊 单人开发时间安排

### 上午（9:00-12:00）

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 9:00-9:30 | 创建所有后端模块目录结构 | 8个模块目录 |
| 9:30-10:30 | 组织管理后端（models/schemas/service/api） | organization后端完成 |
| 10:30-11:30 | AI模型管理后端 | model后端完成 |
| 11:30-12:00 | NL2SQL后端 | nl2sql后端完成 |

### 下午（13:00-17:00）

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 13:00-13:30 | AI技能管理后端 + 系统管理后端 | skill/admin后端完成 |
| 13:30-14:00 | 数字员工后端 + 数据采集后端 | employee/data后端完成 |
| 14:00-14:30 | 即时通讯后端 | im后端完成 |
| 14:30-15:00 | 更新main.py注册所有路由 | 后端路由注册完成 |
| 15:00-16:00 | 组织管理前端 + AI模型管理前端 | organization/model前端完成 |
| 16:00-17:00 | NL2SQL前端 + AI技能管理前端 | nl2sql/skill前端完成 |

### 晚上（19:00-20:00）

| 时间段 | 任务 | 产出 |
|--------|------|------|
| 19:00-19:30 | 更新前端路由配置 | 所有页面可访问 |
| 19:30-20:00 | 前端构建测试 | npm run build通过 |

---

## ✅ Day 2完成标准

1. ✅ 所有8个模块的后端API文件创建完成
2. ✅ 核心模块（P0-P3）前端页面文件创建完成
3. ✅ main.py更新，注册所有路由
4. ✅ 路由配置更新，核心模块页面可访问
5. ✅ 前端构建成功（npm run build）

---

## ⚠️ 注意事项

1. **遵循现有代码风格**：参考auth模块的代码结构和命名规范
2. **统一错误处理**：使用HTTPException返回统一格式错误
3. **权限控制**：所有接口添加get_current_user依赖
4. **软删除支持**：继承BaseModel，使用is_deleted字段
5. **响应格式统一**：使用统一的response_model
6. **前端组件复用**：使用Element Plus组件，保持UI一致性
7. **数据库表设计**：严格遵循init.sql中的表结构定义