# 六堡茶大宗交易市场价格发布系统

> 广西六堡茶大宗交易市场官方价格发布平台

## 📋 系统概述

本系统提供六堡茶大宗交易价格发布功能，包括：
- 📊 大宗单品实时报价
- 📈 数据大屏展示
- 💰 交易统计分析
- 🔔 价格预警功能

## 🏗 系统架构

```
liupao-price-system/
├── server/              # 后端API服务 (Node.js + Express)
├── admin/               # 管理后台 (React + Ant Design)
├── web/                 # 报价展示页面 (React)
├── screen/              # 数据大屏 (HTML + ECharts)
├── mobile/              # 移动端 (PWA)
├── scripts/             # Python数据采集脚本
├── database/            # 数据库脚本
├── docker/              # Docker部署配置
└── docs/                # 文档
```

## 🚀 快速开始

### 环境要求

- Node.js >= 18
- Python >= 3.10
- MySQL >= 8.0
- Redis >= 7.0

### 1. 安装依赖

```bash
# 后端
cd server
npm install

# 管理后台
cd admin
npm install

# 报价展示
cd web
npm install

# 数据大屏
cd screen
npm install
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，填入数据库等信息
```

### 3. 初始化数据库

```bash
mysql -u root -p < database/schema.sql
mysql -u root -p liupao_price < database/seed.sql
```

### 4. 启动服务

```bash
# 后端 (开发)
cd server
npm run dev

# 后端 (生产)
npm run build
npm start

# 管理后台
cd admin
npm start

# 报价展示
cd web
npm start

# 数据大屏
cd screen
npm run dev
```

### 5. 访问系统

- 管理后台: http://localhost:3001/admin
- 报价展示: http://localhost:3001/web
- 数据大屏: http://localhost:3001/screen

## 📦 部署

### Docker 部署

```bash
# 构建并启动所有服务
docker-compose up -d

# 查看日志
docker-compose logs -f

# 停止服务
docker-compose down
```

## 📊 功能模块

### 1. 报价管理
- 产品信息管理
- 每日价格录入
- 价格审核流程
- 历史价格查询

### 2. 数据采集
- API对接
- 网页爬虫
- 手动录入
- 定时任务

### 3. 统计分析
- 日/周/月统计
- 价格趋势
- 排行榜
- 品类分析

### 4. 数据大屏
- 实时价格
- 涨跌分布
- 排行榜
- 交易统计

## 📝 API 文档

详见 [docs/API.md](docs/API.md)

## 🛠 开发

### 项目结构

```
server/
├── src/
│   ├── index.js         # 入口文件
│   ├── app.js           # Express应用
│   ├── config/          # 配置文件
│   ├── models/          # 数据模型
│   ├── routes/          # 路由
│   ├── services/        # 业务逻辑
│   ├── middleware/      # 中间件
│   └── utils/           # 工具函数
└── package.json
```

### 添加新接口

1. 在 `models/` 创建数据模型
2. 在 `routes/` 创建路由文件
3. 在 `services/` 添加业务逻辑
4. 在 `app.js` 注册路由

## 📄 许可证

MIT License
