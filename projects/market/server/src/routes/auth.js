const express = require('express');
const jwt = require('jsonwebtoken');
const bcrypt = require('bcryptjs');
const { User, OperationLog } = require('../models');
const { auth } = require('../middleware/auth');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 登录
router.post('/login', async (req, res) => {
  try {
    const { username, password } = req.body;

    if (!username || !password) {
      return fail(res, '用户名和密码不能为空', 400);
    }

    const user = User.findOne({ username, status: 1 });
    if (!user) {
      return fail(res, '用户不存在或已禁用', 401);
    }

    const validPassword = bcrypt.compareSync(password, user.password);
    if (!validPassword) {
      return fail(res, '密码错误', 401);
    }

    const token = jwt.sign(
      { id: user.id, username: user.username, role: user.role },
      process.env.JWT_SECRET || 'secret',
      { expiresIn: process.env.JWT_EXPIRES_IN || '24h' }
    );

    // 记录登录日志
    OperationLog.create({
      user_id: user.id,
      action: 'LOGIN',
      module: 'auth',
      detail: `用户 ${user.username} 登录成功`,
      ip: req.ip
    });

    success(res, {
      token,
      user: {
        id: user.id,
        username: user.username,
        name: user.name,
        role: user.role
      }
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取当前用户信息
router.get('/me', auth, async (req, res) => {
  try {
    const user = User.findById(req.user.id);
    if (!user) {
      return fail(res, '用户不存在', 404);
    }

    success(res, {
      id: user.id,
      username: user.username,
      name: user.name,
      role: user.role
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 修改密码
router.put('/password', auth, async (req, res) => {
  try {
    const { oldPassword, newPassword } = req.body;

    if (!oldPassword || !newPassword) {
      return fail(res, '旧密码和新密码不能为空', 400);
    }

    const user = User.findById(req.user.id);
    if (!bcrypt.compareSync(oldPassword, user.password)) {
      return fail(res, '旧密码错误', 400);
    }

    const hashedPassword = bcrypt.hashSync(newPassword, 10);
    User.update(req.user.id, { password: hashedPassword });

    OperationLog.create({
      user_id: req.user.id,
      action: 'UPDATE_PASSWORD',
      module: 'auth',
      detail: '用户修改密码',
      ip: req.ip
    });

    success(res, null, '密码修改成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 登出
router.post('/logout', auth, async (req, res) => {
  try {
    OperationLog.create({
      user_id: req.user.id,
      action: 'LOGOUT',
      module: 'auth',
      detail: `用户 ${req.user.username} 登出`,
      ip: req.ip
    });

    success(res, null, '登出成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

module.exports = router;