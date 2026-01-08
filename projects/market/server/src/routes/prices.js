const express = require('express');
const { Price, DailyStatistics } = require('../models');
const { auth, verifyRole } = require('../middleware/auth');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 获取价格列表
router.get('/', (req, res) => {
  try {
    const { page = 1, pageSize = 20, date, category_id, grade_id, year, keyword, sortField, sortOrder } = req.query;

    const conditions = { where: {} };
    if (date) conditions.where.price_date = date;
    if (category_id) conditions.where.category_id = parseInt(category_id);
    if (grade_id) conditions.where.grade_id = parseInt(grade_id);
    if (year) conditions.where.year = parseInt(year);
    if (keyword) conditions.where.product_name = { like: keyword };

    // 排序
    if (sortField && sortOrder) {
      conditions.orderBy = { [sortField]: sortOrder };
    }

    // 分页
    conditions.limit = parseInt(pageSize);
    conditions.offset = (parseInt(page) - 1) * parseInt(pageSize);

    const prices = Price.findAll(conditions);

    // 获取产品信息补充
    const db = require('../config/database');
    const products = db.get('products');

    const pricesWithProduct = prices.map(price => {
      const product = products.find(p => p.id == price.product_id);
      return { ...price, product };
    });

    // 计算总数
    const allPrices = Price.findAll(conditions);

    success(res, {
      list: pricesWithProduct,
      pagination: {
        page: parseInt(page),
        pageSize: parseInt(pageSize),
        total: allPrices.length
      }
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取今日价格
router.get('/today', (req, res) => {
  try {
    const prices = Price.getTodayPrices();

    // 补充产品信息
    const db = require('../config/database');
    const products = db.get('products');

    const pricesWithProduct = prices.map(price => {
      const product = products.find(p => p.id == price.product_id);
      return { ...price, product };
    });

    // 计算统计信息
    const risingCount = prices.filter(p => p.price_change_percent > 0).length;
    const fallingCount = prices.filter(p => p.price_change_percent < 0).length;
    const flatCount = prices.filter(p => p.price_change_percent === 0).length;
    const avgPrice = prices.length > 0 ? prices.reduce((sum, p) => sum + (p.price_avg || 0), 0) / prices.length : 0;

    success(res, {
      list: pricesWithProduct,
      statistics: {
        total: prices.length,
        rising: risingCount,
        falling: fallingCount,
        flat: flatCount,
        avgPrice: avgPrice.toFixed(2)
      }
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取最新价格(实时)
router.get('/latest', (req, res) => {
  try {
    const prices = Price.getLatestPrices();
    success(res, {
      updateTime: new Date().toISOString(),
      prices: prices.map(p => ({
        productId: p.product_id,
        productName: p.product ? p.product.name : '',
        price: p.price_avg,
        changePercent: p.price_change_percent,
        direction: p.price_change_percent > 0 ? 'up' : p.price_change_percent < 0 ? 'down' : 'flat',
        volume: p.volume
      }))
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取历史价格
router.get('/history/:productId', (req, res) => {
  try {
    const { days = 30 } = req.query;
    const history = Price.getHistory(parseInt(req.params.productId), parseInt(days));
    success(res, history);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取单个产品价格
router.get('/:productId', (req, res) => {
  try {
    const { date } = req.query;
    const conditions = { product_id: parseInt(req.params.productId) };
    if (date) conditions.price_date = date;

    const price = Price.findOne(conditions);
    if (!price) {
      return fail(res, '价格不存在', 404);
    }
    success(res, price);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 录入价格
router.post('/', auth, verifyRole(['admin', 'operator']), (req, res) => {
  try {
    const { product_id, price_date, price_buy, price_sell, price_avg, price_change, price_change_percent, volume, turnover, source_id, source_remark } = req.body;

    if (!product_id || !price_date) {
      return fail(res, '产品和日期不能为空', 400);
    }

    // 检查是否已存在该日期的价格
    const existing = Price.findOne({ product_id, price_date });
    if (existing) {
      // 更新
      Price.update(existing.id, {
        price_buy: parseFloat(price_buy) || null,
        price_sell: parseFloat(price_sell) || null,
        price_avg: parseFloat(price_avg) || null,
        price_change: parseFloat(price_change) || null,
        price_change_percent: parseFloat(price_change_percent) || null,
        volume: parseInt(volume) || null,
        turnover: parseFloat(turnover) || null,
        source_id: parseInt(source_id) || null,
        source_remark,
        status: 0 // 待审核
      });
      const updated = Price.findById(existing.id);
      return success(res, updated, '更新成功');
    }

    const price = Price.create({
      product_id: parseInt(product_id),
      price_date,
      price_buy: parseFloat(price_buy) || null,
      price_sell: parseFloat(price_sell) || null,
      price_avg: parseFloat(price_avg) || null,
      price_change: parseFloat(price_change) || null,
      price_change_percent: parseFloat(price_change_percent) || null,
      volume: parseInt(volume) || null,
      turnover: parseFloat(turnover) || null,
      source_id: parseInt(source_id) || null,
      source_type: 'manual',
      source_remark,
      status: 0 // 待审核
    });

    success(res, price, '录入成功', 201);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 更新价格
router.put('/:id', auth, verifyRole(['admin', 'operator']), (req, res) => {
  try {
    const price = Price.findById(req.params.id);
    if (!price) {
      return fail(res, '价格不存在', 404);
    }

    Price.update(req.params.id, {
      ...req.body,
      status: 0 // 重新提交审核
    });
    const updated = Price.findById(req.params.id);
    success(res, updated, '更新成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 删除价格
router.delete('/:id', auth, verifyRole(['admin']), (req, res) => {
  try {
    const price = Price.findById(req.params.id);
    if (!price) {
      return fail(res, '价格不存在', 404);
    }

    Price.delete(req.params.id);
    success(res, null, '删除成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取待审核价格
router.get('/verify/pending', auth, verifyRole(['admin', 'manager']), (req, res) => {
  try {
    const prices = Price.getPendingPrices();

    // 补充产品信息
    const db = require('../config/database');
    const products = db.get('products');

    const pricesWithProduct = prices.map(price => {
      const product = products.find(p => p.id == price.product_id);
      return { ...price, product };
    });

    success(res, pricesWithProduct);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 审核价格
router.post('/verify', auth, verifyRole(['admin', 'manager']), (req, res) => {
  try {
    const { id, status } = req.body;

    const price = Price.findById(id);
    if (!price) {
      return fail(res, '价格不存在', 404);
    }

    Price.verify(id, req.user.id);
    const updated = Price.findById(id);

    success(res, updated, status === 1 ? '审核通过' : '已驳回');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

module.exports = router;