/**
 * 广西六堡茶大宗交易市场价格发布系统 - 后端入口
 */

require('dotenv').config();
const express = require('express');
const cors = require('cors');
const helmet = require('helmet');
const morgan = require('morgan');
const compression = require('compression');

const routes = require('./routes');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');
const { logger } = require('./utils/logger');

const app = express();
const PORT = process.env.PORT || 3000;

// 中间件配置
app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGIN || '*',
  credentials: true
}));
app.use(compression());
app.use(morgan('combined', { stream: { write: (msg) => logger.info(msg.trim()) } }));
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// 静态文件服务
app.use('/uploads', express.static('uploads'));

// API路由
app.use('/api/v1', routes);

// 健康检查
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: new Date().toISOString() });
});

// 错误处理
app.use(notFoundHandler);
app.use(errorHandler);

// 启动服务
app.listen(PORT, () => {
  logger.info(`🚀 六堡茶价格发布系统服务已启动`);
  logger.info(`📡 服务端口: ${PORT}`);
  logger.info(`🌐 环境: ${process.env.NODE_ENV || 'development'}`);
});

module.exports = app;
