/**
 * 认证中间件
 */

const jwt = require('jsonwebtoken');
const { User } = require('../models');

// 验证Token
const auth = async (req, res, next) => {
  try {
    const authHeader = req.headers.authorization;

    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ code: 401, message: '未提供认证Token' });
    }

    const token = authHeader.split(' ')[1];
    const secret = process.env.JWT_SECRET || 'secret';
    const decoded = jwt.verify(token, secret);

    const user = User.findById(decoded.id);
    if (!user) {
      return res.status(401).json({ code: 401, message: '用户不存在' });
    }

    if (user.status !== 1) {
      return res.status(403).json({ code: 403, message: '账户已被禁用' });
    }

    req.user = decoded;
    next();
  } catch (error) {
    return res.status(401).json({ code: 401, message: '认证失败' });
  }
};

// 角色权限检查
const verifyRole = (...roles) => {
  return (req, res, next) => {
    if (!req.user) {
      return res.status(401).json({ code: 401, message: '未登录' });
    }

    if (!roles.includes(req.user.role)) {
      return res.status(403).json({ code: 403, message: '没有操作权限' });
    }

    next();
  };
};

module.exports = { auth, verifyRole };