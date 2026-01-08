const express = require('express');
const { Price, DailyStatistics } = require('../models');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 日统计
router.get('/daily', (req, res) => {
  try {
    const { date } = req.query;
    if (date) {
      const stat = DailyStatistics.findByDate(date);
      success(res, stat || null);
    } else {
      const stats = DailyStatistics.findAll({
        orderBy: { stat_date: 'desc' },
        limit: 30
      });
      success(res, stats);
    }
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 趋势数据
router.get('/trend', (req, res) => {
  try {
    const { productId, startDate, endDate, period = 'day' } = req.query;
    const db = require('../config/database');
    const prices = db.get('daily_prices');

    let filtered = [...prices];

    // 按产品筛选
    if (productId) {
      filtered = filtered.filter(p => p.product_id == productId);
    }

    // 按日期范围筛选
    if (startDate) {
      filtered = filtered.filter(p => p.price_date >= startDate);
    }
    if (endDate) {
      filtered = filtered.filter(p => p.price_date <= endDate);
    }

    // 按日期分组计算均值
    const trendMap = {};
    filtered.forEach(p => {
      if (!trendMap[p.price_date]) {
        trendMap[p.price_date] = { date: p.price_date, prices: [], volume: 0, turnover: 0 };
      }
      trendMap[p.price_date].prices.push(p.price_avg || 0);
      trendMap[p.price_date].volume += p.volume || 0;
      trendMap[p.price_date].turnover += p.turnover || 0;
    });

    const trend = Object.values(trendMap)
      .map(item => ({
        date: item.date,
        avgPrice: item.prices.length > 0 ? (item.prices.reduce((a, b) => a + b, 0) / item.prices.length).toFixed(2) : 0,
        volume: item.volume,
        turnover: item.turnover
      }))
      .sort((a, b) => new Date(a.date) - new Date(b.date));

    // 计算统计信息
    const allPrices = filtered.map(p => p.price_avg || 0).filter(p => p > 0);
    const statistics = {
      avgPrice: allPrices.length > 0 ? (allPrices.reduce((a, b) => a + b, 0) / allPrices.length).toFixed(2) : 0,
      maxPrice: allPrices.length > 0 ? Math.max(...allPrices).toFixed(2) : 0,
      minPrice: allPrices.length > 0 ? Math.min(...allPrices).toFixed(2) : 0,
      totalVolume: filtered.reduce((sum, p) => sum + (p.volume || 0), 0),
      totalTurnover: filtered.reduce((sum, p) => sum + (p.turnover || 0), 0)
    };

    // 获取产品信息
    let product = null;
    if (productId) {
      const products = db.get('products');
      product = products.find(p => p.id == productId);
    }

    success(res, { product, trend, statistics });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 排行榜
router.get('/rankings', (req, res) => {
  try {
    const { type = 'rising', limit = 10 } = req.query;
    const db = require('../config/database');
    const prices = db.get('daily_prices');
    const products = db.get('products');

    // 获取今日价格
    const today = new Date().toISOString().split('T')[0];
    const todayPrices = prices.filter(p => p.price_date === today);

    // 排序
    let sorted;
    if (type === 'rising') {
      sorted = todayPrices.sort((a, b) => (b.price_change_percent || 0) - (a.price_change_percent || 0));
    } else if (type === 'falling') {
      sorted = todayPrices.sort((a, b) => (a.price_change_percent || 0) - (b.price_change_percent || 0));
    } else if (type === 'volume') {
      sorted = todayPrices.sort((a, b) => (b.volume || 0) - (a.volume || 0));
    } else if (type === 'turnover') {
      sorted = todayPrices.sort((a, b) => (b.turnover || 0) - (a.turnover || 0));
    }

    const rankings = sorted.slice(0, parseInt(limit)).map(p => {
      const product = products.find(prod => prod.id == p.product_id);
      return {
        ...p,
        product_name: product ? product.name : '',
        product_code: product ? product.code : ''
      };
    });

    success(res, rankings);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 品类统计
router.get('/category', (req, res) => {
  try {
    const db = require('../config/database');
    const prices = db.get('daily_prices');
    const categories = db.get('product_categories');

    // 获取今日价格
    const today = new Date().toISOString().split('T')[0];
    const todayPrices = prices.filter(p => p.price_date === today);

    // 按品类分组统计
    const categoryStats = categories.map(cat => {
      const catPrices = todayPrices.filter(p => p.category_id == cat.id);
      const avgPrice = catPrices.length > 0
        ? catPrices.reduce((sum, p) => sum + (p.price_avg || 0), 0) / catPrices.length
        : 0;

      const rising = catPrices.filter(p => (p.price_change_percent || 0) > 0).length;
      const falling = catPrices.filter(p => (p.price_change_percent || 0) < 0).length;

      return {
        category_id: cat.id,
        category_name: cat.name,
        count: catPrices.length,
        avgPrice: avgPrice.toFixed(2),
        rising,
        falling
      };
    });

    success(res, categoryStats);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 整体概览
router.get('/overview', (req, res) => {
  try {
    const db = require('../config/database');
    const prices = db.get('daily_prices');
    const products = db.get('products');

    // 获取今日价格
    const today = new Date().toISOString().split('T')[0];
    const todayPrices = prices.filter(p => p.price_date === today);

    const rising = todayPrices.filter(p => (p.price_change_percent || 0) > 0).length;
    const falling = todayPrices.filter(p => (p.price_change_percent || 0) < 0).length;
    const flat = todayPrices.length - rising - falling;

    const totalVolume = todayPrices.reduce((sum, p) => sum + (p.volume || 0), 0);
    const totalTurnover = todayPrices.reduce((sum, p) => sum + (p.turnover || 0), 0);
    const avgPrice = todayPrices.length > 0
      ? todayPrices.reduce((sum, p) => sum + (p.price_avg || 0), 0) / todayPrices.length
      : 0;

    // 计算价格指数(以某个基数为100)
    const priceIndex = avgPrice > 0 ? ((avgPrice / 280) * 100).toFixed(2) : 100;

    success(res, {
      date: today,
      totalProducts: products.length,
      todayCount: todayPrices.length,
      rising,
      falling,
      flat,
      avgPrice: avgPrice.toFixed(2),
      totalVolume,
      totalTurnover,
      priceIndex
    });
  } catch (error) {
    fail(res, error.message, 500);
  }
});

module.exports = router;