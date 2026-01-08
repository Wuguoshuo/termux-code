const express = require('express');
const db = require('../config/database');
const { auth, verifyRole } = require('../middleware/auth');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 获取数据源列表
router.get('/', (req, res) => {
  try {
    const sources = db.query('data_sources', {
      orderBy: { id: 'asc' }
    });
    success(res, sources);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取单个数据源
router.get('/:id', (req, res) => {
  try {
    const source = db.findById('data_sources', req.params.id);
    if (!source) {
      return fail(res, '数据源不存在', 404);
    }
    success(res, source);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 创建数据源
router.post('/', auth, verifyRole(['admin']), (req, res) => {
  try {
    const { name, type, api_url, api_key, api_secret, auth_type, selector_config, field_mapping, crawl_schedule, retry_times, retry_interval } = req.body;

    if (!name || !type) {
      return fail(res, '名称和类型不能为空', 400);
    }

    const source = db.insert('data_sources', {
      name,
      type,
      api_url,
      api_key,
      api_secret,
      auth_type,
      selector_config,
      field_mapping,
      crawl_schedule,
      retry_times: parseInt(retry_times) || 3,
      retry_interval: parseInt(retry_interval) || 300,
      status: 1
    });

    success(res, source, '创建成功', 201);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 更新数据源
router.put('/:id', auth, verifyRole(['admin']), (req, res) => {
  try {
    const source = db.findById('data_sources', req.params.id);
    if (!source) {
      return fail(res, '数据源不存在', 404);
    }

    db.update('data_sources', req.params.id, {
      ...req.body,
      updated_at: new Date().toISOString()
    });
    const updated = db.findById('data_sources', req.params.id);
    success(res, updated, '更新成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 删除数据源
router.delete('/:id', auth, verifyRole(['admin']), (req, res) => {
  try {
    const source = db.findById('data_sources', req.params.id);
    if (!source) {
      return fail(res, '数据源不存在', 404);
    }

    db.delete('data_sources', req.params.id);
    success(res, null, '删除成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 测试数据源连接
router.post('/:id/test', auth, verifyRole(['admin']), (req, res) => {
  try {
    const source = db.findById('data_sources', req.params.id);
    if (!source) {
      return fail(res, '数据源不存在', 404);
    }

    // TODO: 实现实际的连接测试
    success(res, { success: true, message: '连接测试成功(模拟)' });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 手动触发同步
router.post('/:id/sync', auth, verifyRole(['admin', 'operator']), (req, res) => {
  try {
    const source = db.findById('data_sources', req.params.id);
    if (!source) {
      return fail(res, '数据源不存在', 404);
    }

    // 更新最后运行时间
    db.update('data_sources', req.params.id, {
      last_run_at: new Date().toISOString()
    });

    // TODO: 实现实际的数据同步
    success(res, { success: true, message: '同步任务已启动(模拟)' });
  } catch (error) {
    db.update('data_sources', req.params.id, {
      last_run_at: new Date().toISOString(),
      error_message: error.message
    });
    fail(res, error.message, 500);
  }
});

module.exports = router;