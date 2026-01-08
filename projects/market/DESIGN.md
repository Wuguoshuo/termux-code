# 六堡茶大宗交易市场价格发布系统 - 设计文档

## 一、项目概述

### 1.1 项目背景
广西六堡茶大宗交易市场需要一个专业的价格发布系统，参考东和茶仓模式，提供大宗单品报价、数据大屏展示等功能。

### 1.2 系统定位
- **核心功能**: 大宗单品报价、实时数据大屏、交易统计
- **目标用户**: 茶商、投资者、市场管理者
- **终端覆盖**: PC管理端、PC展示端、数据大屏、移动端

---

## 二、技术架构

### 2.1 技术选型

| 层级 | 技术方案 | 说明 |
|------|----------|------|
| **后端** | Node.js + Express | RESTful API服务 |
| **数据库** | SQLite (开发) / MySQL (生产) | 数据持久化 |
| **管理后台** | React + Ant Design | 后台管理系统 |
| **展示页面** | React + ECharts | 报价展示、趋势分析 |
| **数据大屏** | 原生JS + ECharts | 大屏可视化 |
| **移动端** | React PWA | 移动端轻量访问 |
| **数据采集** | Python + sql.js | ETL数据处理 |

### 2.2 系统架构图

```
┌─────────────────────────────────────────────────────────────────────┐
│                         客户端层                                     │
├─────────────────┬─────────────────┬─────────────────┬───────────────┤
│   管理后台      │   Web展示页     │   数据大屏      │   移动端      │
│   (React)      │   (React)       │   (ECharts)     │   (PWA)       │
└────────┬────────┴────────┬────────┴────────┬────────┴───────┬───────┘
         │                 │                 │                │
         └─────────────────┴─────────────────┴────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        API Gateway (Nginx)                          │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          后端服务层                                  │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐               │
│  │ Auth    │  │ Product │  │  Price  │  │ Statistics│             │
│  │ 认证服务 │  │ 产品服务 │  │ 价格服务 │  │ 统计服务 │               │
│  └─────────┘  └─────────┘  └─────────┘  └─────────┘               │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                          数据存储层                                  │
│  ┌─────────────────┐  ┌─────────────────┐                          │
│  │    SQLite       │  │   文件存储      │                          │
│  │   (data/*.db)   │  │   (logs/)       │                          │
│  └─────────────────┘  └─────────────────┘                          │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 三、数据库设计

### 3.1 数据表结构

#### 3.1.1 产品基础表 (products)
```sql
CREATE TABLE products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR(30) UNIQUE NOT NULL,      -- 产品编码 LP-2024-001
    name VARCHAR(100) NOT NULL,            -- 品名
    category VARCHAR(50),                  -- 类别: 散茶/紧压茶/年份茶
    grade VARCHAR(20),                     -- 等级: 特级/一级/二级
    year INTEGER,                          -- 年份
    origin VARCHAR(50),                    -- 产地: 梧州/横州/桂林
    spec VARCHAR(50),                      -- 规格: 1kg/10kg/件
    brand VARCHAR(100),                    -- 品牌
    status INTEGER DEFAULT 1,              -- 状态: 0-停用 1-正常
    sort_order INTEGER DEFAULT 0,          -- 排序
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.2 每日价格表 (daily_prices)
```sql
CREATE TABLE daily_prices (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    product_id INTEGER NOT NULL,
    price_date DATE NOT NULL,              -- 报价日期
    
    -- 价格信息
    price_buy DECIMAL(12,2),               -- 买入价(最低)
    price_sell DECIMAL(12,2),              -- 卖出价(最高)
    price_avg DECIMAL(12,2),               -- 均价
    price_change DECIMAL(12,2),            -- 涨跌额
    price_change_percent DECIMAL(8,4),     -- 涨跌幅%
    
    -- 交易信息
    volume INTEGER,                        -- 成交量
    turnover DECIMAL(15,2),                -- 成交额(元)
    volume_unit VARCHAR(20),               -- 成交量单位
    
    -- 数据来源
    source_id INTEGER,                     -- 来源ID
    source_type VARCHAR(20),               -- api/manual/crawler
    source_remark VARCHAR(200),            -- 来源备注
    
    -- 审核状态
    status INTEGER DEFAULT 1,              -- 0-待审核 1-已发布 2-已驳回
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (product_id) REFERENCES products(id),
    UNIQUE(product_id, price_date)
);
```

#### 3.1.3 用户表 (users)
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    name VARCHAR(50),
    role VARCHAR(20) DEFAULT 'viewer',     -- admin/manager/operator/viewer
    status INTEGER DEFAULT 1,
    last_login DATETIME,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.4 数据源配置表 (data_sources)
```sql
CREATE TABLE data_sources (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    type VARCHAR(20) NOT NULL,             -- api/manual/crawler
    api_url VARCHAR(500),
    api_key VARCHAR(255),
    config TEXT,                           -- JSON配置
    status INTEGER DEFAULT 1,
    last_run_at DATETIME,
    last_success_at DATETIME,
    error_message TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.5 系统配置表 (system_config)
```sql
CREATE TABLE system_config (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    key VARCHAR(100) UNIQUE NOT NULL,
    value TEXT,
    type VARCHAR(20) DEFAULT 'string',
    description VARCHAR(200),
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

#### 3.1.6 日统计数据表 (daily_statistics)
```sql
CREATE TABLE daily_statistics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stat_date DATE NOT NULL,
    
    -- 整体统计
    total_products INTEGER,                -- 报价品种数
    rising_count INTEGER,                  -- 上涨数
    falling_count INTEGER,                 -- 下跌数
    flat_count INTEGER,                    -- 持平数
    
    -- 价格统计
    avg_price DECIMAL(12,2),               -- 整体均价
    max_price DECIMAL(12,2),               -- 最高价
    min_price DECIMAL(12,2),               -- 最低价
    
    -- 交易统计
    total_volume INTEGER,                  -- 总成交量
    total_turnover DECIMAL(18,2),          -- 总成交额
    
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stat_date)
);
```

---

## 四、API接口设计

### 4.1 基础路径
```
http://localhost:3000/api/v1
```

### 4.2 接口列表

| 方法 | 路径 | 说明 | 权限 |
|------|------|------|------|
| **系统** |
| GET | /system/health | 健康检查 | 公开 |
| **认证** |
| POST | /auth/login | 用户登录 | 公开 |
| GET | /auth/profile | 获取用户信息 | 需要认证 |
| **产品** |
| GET | /products | 获取产品列表 | 公开 |
| GET | /products/:id | 获取产品详情 | 公开 |
| POST | /products | 创建产品 | admin |
| PUT | /products/:id | 更新产品 | admin |
| DELETE | /products/:id | 删除产品 | admin |
| **价格** |
| GET | /prices/today | 获取今日价格 | 公开 |
| GET | /prices | 获取价格列表(筛选) | 公开 |
| GET | /prices/:id | 获取价格详情 | 公开 |
| GET | /prices/:id/history | 获取历史价格 | 公开 |
| POST | /prices | 录入价格 | operator+ |
| PUT | /prices/:id | 更新价格 | operator+ |
| DELETE | /prices/:id | 删除价格 | admin |
| POST | /prices/verify | 审核价格 | manager+ |
| GET | /prices/verify/pending | 待审核列表 | manager+ |
| **统计** |
| GET | /statistics/overview | 概览统计 | 公开 |
| GET | /statistics/category | 品类统计 | 公开 |
| GET | /statistics/rankings | 排行榜 | 公开 |
| GET | /statistics/trend | 趋势数据 | 公开 |
| **数据源** |
| GET | /sources | 获取数据源列表 | manager |
| POST | /sources | 创建数据源 | admin |
| PUT | /sources/:id | 更新数据源 | admin |
| DELETE | /sources/:id | 删除数据源 | admin |
| POST | /sources/:id/test | 测试数据源 | admin |
| POST | /sources/:id/sync | 手动同步 | admin |
| **系统** |
| GET | /system/config | 获取系统配置 | manager |
| PUT | /system/config | 更新系统配置 | admin |

### 4.3 响应格式

```json
// 成功响应
{
    "code": 200,
    "message": "success",
    "data": { ... }
}

// 分页响应
{
    "code": 200,
    "message": "success",
    "data": {
        "list": [...],
        "pagination": {
            "page": 1,
            "pageSize": 20,
            "total": 156
        }
    }
}

// 错误响应
{
    "code": 400,
    "message": "参数错误",
    "error": "详细错误信息"
}
```

---

## 五、功能模块设计

### 5.1 管理后台 (admin/)

| 页面 | 功能 |
|------|------|
| **登录页** | 用户登录、记住密码 |
| **仪表盘** | 今日数据概览、价格走势图、快捷入口 |
| **产品管理** | 产品列表、搜索筛选、新增/编辑/删除 |
| **报价管理** | 今日报价列表、筛选、录入、编辑 |
| **价格审核** | 待审核列表、审核通过/驳回 |
| **数据源管理** | 数据源配置、手动同步 |
| **系统设置** | 系统参数配置 |

### 5.2 报价展示页 (web/)

| 页面 | 功能 |
|------|------|
| **首页/大盘** | 行情概览、涨跌分布、品类统计 |
| **今日报价** | 报价列表、搜索筛选、排序 |
| **走势分析** | 价格趋势图、交易量图 |

### 5.3 数据大屏 (screen/)

| 模块 | 说明 |
|------|------|
| **价格指数** | 实时价格指数、涨跌幅 |
| **涨跌分布** | 上涨/下跌/持平数量统计 |
| **品类行情** | 各品类价格对比 |
| **涨幅/跌幅榜** | TOP10排名 |
| **价格滚动** | 实时价格滚动展示 |

### 5.4 移动端 (mobile/)

| 页面 | 功能 |
|------|------|
| **首页** | 今日行情概览、快捷入口 |
| **报价查询** | 产品搜索、价格查看 |
| **价格提醒** | 涨跌预警设置 |

---

## 六、权限体系

### 6.1 角色定义

| 角色 | 说明 | 权限范围 |
|------|------|----------|
| **admin** | 管理员 | 全部权限 |
| **manager** | 部门主管 | 录入、审核、管理 |
| **operator** | 操作员 | 录入、编辑 |
| **viewer** | 查看者 | 只读 |

### 6.2 权限矩阵

| 功能 | admin | manager | operator | viewer |
|------|-------|---------|----------|--------|
| 产品管理 | CRUD | R | R | R |
| 价格管理 | CRUD | CRUD | CRU | R |
| 价格审核 | ✓ | ✓ | ✗ | ✗ |
| 数据源管理 | CRUD | R | R | R |
| 系统配置 | ✓ | R | R | R |
| 统计报表 | ✓ | ✓ | ✓ | ✓ |

---

## 七、数据采集设计

### 7.1 混合采集模式

```
┌─────────────────────────────────────────────────────────────────────┐
│                        数据采集层                                    │
├─────────────────┬─────────────────┬─────────────────────────────────┤
│    API对接      │    网页爬虫      │        人工录入                  │
│      (自动)     │      (自动)      │         (手动)                  │
├─────────────────┼─────────────────┼─────────────────────────────────┤
│ • 东和茶仓API   │ • 各大茶业网站   │ • 电话询价记录                  │
│ • 茶交所行情    │ • 行业资讯平台   │ • 经销商报价                    │
│ • 产地直供数据  │                  │ • 展会报价                      │
└────────┬────────┴────────┬────────┴─────────────────────────────────┘
         │                 │
         ▼                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                     ETL 处理管道                                     │
│  Extract → Transform → Validate → Load                              │
└────────────────────────────────┬────────────────────────────────────┘
                                 │
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│                       审核发布流程                                    │
│  数据录入 → 系统校验 → 待审核 → 审核通过 → 价格发布                    │
└─────────────────────────────────────────────────────────────────────┘
```

### 7.2 定时任务

| 任务 | 调度 | 说明 |
|------|------|------|
| 价格采集 | 9:00, 14:00 | 自动采集外部数据 |
| 日统计 | 23:00 | 生成每日统计 |
| 数据快照 | 每小时 | 保存历史快照 |
| 预警检测 | 每5分钟 | 检测价格预警 |

---

## 八、部署架构

### 8.1 开发环境

```
本地开发:
├── 后端: http://localhost:3000
├── 管理后台: http://localhost:3001
├── 数据库: SQLite (data/liupao.db)
└── 日志: logs/app.log
```

### 8.2 生产环境(推荐)

```
┌─────────────────────────────────────────────────────────────────────┐
│                          生产环境部署                                │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐     ┌─────────────┐                               │
│  │   Web端     │     │   大屏端    │                               │
│  └──────┬──────┘     └──────┬──────┘                               │
│         │                    │                                      │
│         └─────────┬──────────┘                                      │
│                   ▼                                                 │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Nginx (负载均衡)                          │   │
│  └───────────────────────────┬─────────────────────────────────┘   │
│                              │                                       │
│         ┌────────────────────┼────────────────────┐                │
│         ▼                    ▼                    ▼                │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐          │
│  │  API Server  │   │  API Server  │   │  API Server  │          │
│  └──────┬───────┘   └──────┬───────┘   └──────┬───────┘          │
│         │                  │                  │                    │
│         └──────────────────┼──────────────────┘                    │
│                            ▼                                       │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    MySQL Cluster                             │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 九、项目结构

```
projects/market/
├── README.md                    # 项目说明
├── .env.example                 # 环境变量模板
│
├── server/                      # 后端服务
│   ├── package.json
│   ├── src/
│   │   ├── index.js             # 入口
│   │   ├── app.js               # Express应用
│   │   ├── config/              # 配置
│   │   ├── models/              # 数据模型
│   │   ├── routes/              # API路由
│   │   ├── middleware/          # 中间件
│   │   └── utils/               # 工具函数
│   ├── data/                    # 数据库文件
│   ├── logs/                    # 日志文件
│   └── scripts/                 # 脚本
│
├── admin/                       # 管理后台
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── index.js
│       ├── App.jsx
│       ├── api/                 # API调用
│       ├── components/          # 组件
│       └── pages/               # 页面
│
├── web/                         # 报价展示页
│   ├── package.json
│   └── src/
│       ├── index.js
│       └── pages/               # 页面
│
├── screen/                      # 数据大屏
│   ├── package.json
│   └── public/
│       ├── index.html
│       └── screen.js
│
├── mobile/                      # 移动端
│   ├── package.json
│   └── public/
│       └── index.html
│
├── scripts/                     # Python脚本
│   ├── requirements.txt
│   └── etl/
│       └── pipeline.py
│
├── database/                    # 数据库
│   ├── schema.sql               # 表结构
│   └── seed.sql                 # 初始数据
│
└── docker/                      # Docker配置
    ├── docker-compose.yml
    ├── Dockerfile.server
    └── nginx.conf
```

---

## 十、运行指南

### 10.1 环境要求

- Node.js >= 18
- npm >= 9
- Python >= 3.8 (可选，用于数据采集)

### 10.2 快速启动

```bash
# 1. 安装依赖
cd server && npm install
cd ../admin && npm install
cd ../web && npm install

# 2. 初始化数据库
cd server && node scripts/init-db.js

# 3. 启动后端
cd server && npm run dev

# 4. 启动管理后台
cd admin && npm start

# 5. 启动展示页面
cd web && npm start
```

### 10.3 Docker部署

```bash
cd docker
docker-compose up -d
```

---

## 十一、默认账号

| 角色 | 用户名 | 密码 |
|------|--------|------|
| 管理员 | admin | admin123 |
| 主管 | manager | manager123 |
| 操作员 | operator | operator123 |
| 查看者 | viewer | viewer123 |

---

## 十二、后续扩展

- [ ] 微信小程序
- [ ] 价格预警推送
- [ ] 数据导出功能
- [ ] 多数据源对接
- [ ] AI价格预测
