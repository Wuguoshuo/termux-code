/**
 * 错误处理中间件
 */

const { logger } = require('../utils/logger');

// 404处理
const notFoundHandler = (req, res, next) => {
  res.status(404).json({
    code: 404,
    message: '请求的资源不存在'
  });
};

// 全局错误处理
const errorHandler = (err, req, res, next) => {
  logger.error('请求错误:', {
    error: err.message,
    stack: err.stack,
    url: req.url,
    method: req.method
  });

  // 参数校验错误
  if (err.array && typeof err.array === 'function') {
    return res.status(400).json({
      code: 400,
      message: '参数错误',
      errors: err.array()
    });
  }

  // JWT错误
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      code: 401,
      message: '无效的Token'
    });
  }

  if (err.name === 'TokenExpiredError') {
    return res.status(401).json({
      code: 401,
      message: 'Token已过期'
    });
  }

  // 数据库错误
  if (err.name === 'SequelizeUniqueConstraintError') {
    return res.status(400).json({
      code: 400,
      message: '数据已存在，请勿重复添加'
    });
  }

  // 默认错误响应
  const statusCode = err.statusCode || 500;
  res.status(statusCode).json({
    code: statusCode,
    message: process.env.NODE_ENV === 'production' 
      ? '服务器内部错误' 
      : err.message
  });
};

module.exports = { notFoundHandler, errorHandler };
