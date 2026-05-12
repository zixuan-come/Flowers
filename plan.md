# Flowers - 脚本花园

## 概念
每个脚本是一朵花，网站是一座花园。所有人可浏览，增删改需密码验证。

---

## 技术栈

| 层 | 技术 |
|---|---|
| 后端 | Python + FastAPI |
| 数据库 | MySQL |
| 前端 | Vue 3 + Vite + TailwindCSS |
| 部署 | Docker Compose（前端 Nginx + 后端 + MySQL） |

---

## 数据库设计

### categories 表（分类）
| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT AUTO_INCREMENT | 主键 |
| name | VARCHAR(50) | 分类名，如"爬虫"、"自动化"、"数据处理" |
| icon | VARCHAR(50) | 分类图标（emoji 或 icon name） |
| sort_order | INT | 排序 |
| created_at | DATETIME | 创建时间 |

### scripts 表（脚本/花朵）
| 字段 | 类型 | 说明 |
|---|---|---|
| id | INT AUTO_INCREMENT | 主键 |
| title | VARCHAR(100) | 脚本名称 |
| description | TEXT | 用途说明 |
| language | VARCHAR(20) | 语言（Python/Shell/JS 等） |
| code | LONGTEXT | 脚本内容 |
| category_id | INT | 所属分类，外键 |
| tags | VARCHAR(200) | 标签，逗号分隔 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

---

## API 设计

### 公开接口（无需密码）
- `GET /api/scripts` — 获取脚本列表（支持分页、分类筛选、搜索）
- `GET /api/scripts/{id}` — 获取脚本详情
- `GET /api/categories` — 获取所有分类

### 受保护接口（需要密码，通过请求头 `X-Admin-Password` 传递）
- `POST /api/scripts` — 上传脚本
- `PUT /api/scripts/{id}` — 修改脚本
- `DELETE /api/scripts/{id}` — 删除脚本
- `POST /api/categories` — 新增分类
- `PUT /api/categories/{id}` — 修改分类
- `DELETE /api/categories/{id}` — 删除分类
- `POST /api/verify-password` — 验证密码（前端用，验证后本地缓存）

---

## 前端页面设计

### 整体风格
- **花园主题**：柔和渐变背景，卡片式布局，每朵"花"是一张卡片
- 配色：暖色系渐变（淡粉 → 淡紫 → 淡蓝），白色卡片
- 字体：中文用思源黑体/系统默认，代码用 JetBrains Mono
- 动效：卡片 hover 微浮起，页面切换有过渡动画

### 页面结构（单页应用）

#### 1. 首页 / 花园
- 顶部：标题 "Flowers 🌸" + 搜索框 + 分类筛选标签
- 主体：瀑布流/网格卡片，每张卡片展示：
  - 脚本名称
  - 语言标签（带颜色）
  - 简短描述
  - 分类标签
  - 创建时间
- 右下角浮动按钮 "+" 用于新增（点击后弹出密码验证）

#### 2. 脚本详情（弹窗或新页面）
- 完整描述
- 代码高亮展示（使用 highlight.js 或 Shiki）
- 一键复制按钮
- 编辑/删除按钮（需密码）

#### 3. 管理模式
- 不做单独页面，所有管理操作通过弹窗完成
- 首次操作时弹出密码输入框
- 密码验证通过后，本次会话内（sessionStorage）不再重复询问
- 支持：新增脚本、编辑脚本、删除脚本、管理分类

---

## 项目目录结构

```
flowers/
├── docker-compose.yml
├── backend/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── app/
│   │   ├── main.py              # FastAPI 入口
│   │   ├── config.py            # 配置（密码、数据库连接）
│   │   ├── database.py          # 数据库连接
│   │   ├── models.py            # SQLAlchemy 模型
│   │   ├── schemas.py           # Pydantic schemas
│   │   ├── dependencies.py      # 密码验证依赖
│   │   └── routers/
│   │       ├── scripts.py       # 脚本 CRUD
│   │       └── categories.py    # 分类 CRUD
│   └── alembic/                 # 数据库迁移（可选）
├── frontend/
│   ├── Dockerfile
│   ├── nginx.conf
│   ├── package.json
│   ├── vite.config.js
│   ├── index.html
│   ├── src/
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── api/                 # API 调用封装
│   │   ├── components/          # 组件
│   │   ├── views/               # 页面
│   │   ├── stores/              # Pinia 状态管理
│   │   └── assets/              # 样式资源
│   └── public/
└── mysql/
    └── init.sql                 # 数据库初始化
```

---

## Docker 部署

docker-compose.yml 包含三个服务：
- **mysql**: MySQL 8.0，挂载数据卷持久化
- **backend**: FastAPI 应用，依赖 mysql
- **frontend**: Nginx 托管前端静态文件 + 反向代理后端 API

---

## 实施步骤

1. **初始化项目结构** — 创建目录和配置文件
2. **后端开发** — 数据库模型、API 接口、密码验证
3. **前端开发** — Vue 项目、页面组件、API 对接
4. **Docker 配置** — Dockerfile、docker-compose、nginx 配置
5. **联调测试**
