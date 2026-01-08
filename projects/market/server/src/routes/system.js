const express = require('express');
const db = require('../config/database');
const { auth, verifyRole } = require('../middleware/auth');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 获取系统配置
router.get('/config', (req, res) => {
  try {
    const configs = db.query('system_config');
    const configMap = {};
    configs.forEach(c => {
      configMap[c.key] = c.value;
    });
    success(res, configMap);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 更新系统配置
router.put('/config', auth, verifyRole(['admin']), (req, res) => {
  try {
    const { key, value, type, description } = req.body;

    if (!key) {
      return fail(res, '配置键不能为空', 400);
    }

    const existing = db.findOne('system_config', { key });
    if (existing) {
      db.update('system_config', existing.id, {
        value,
        type: type || 'string',
        description,
        updated_at: new Date().toISOString()
      });
    } else {
      db.insert('system_config', {
        key,
        value,
        type: type || 'string',
        description
      });
    }

    success(res, null, '配置更新成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 系统运行统计
router.get('/stats', auth, (req, res) => {
  try {
    const products = db.get('products');
    const prices = db.get('daily_prices');
    const users = db.get('users');
    const sources = db.get('data_sources');

    // 今日价格数量
    const today = new Date().toISOString().split('T')[0];
    const todayPrices = prices.filter(p => p.price_date === today).length;

    // 待审核数量
    const pendingPrices = prices.filter(p => p.status === 0).length;

    // 活跃用户数
    const activeUsers = users.filter(u => u.status === 1).length;

    success(res, {
      totalProducts: products.length,
      totalPrices: prices.length,
      todayPrices,
      pendingPrices,
      totalUsers: users.length,
      activeUsers,
      totalSources: sources.length,
      uptime: process.uptime()
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 健康检查
router.get('/health', (req, res) => {
  success(res, {
    status: 'ok',
    timestamp: new Date().toISOString(),
    uptime: process.uptime()
  });
});

module.exports = router;