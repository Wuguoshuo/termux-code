const db = require('../config/database');

// 价格模型
const Price = {
  // 获取所有价格
  findAll(conditions = {}) {
    return db.query('daily_prices', conditions);
  },

  // 根据条件查找
  findOne(conditions) {
    return db.findOne('daily_prices', conditions);
  },

  // 根据ID查找
  findById(id) {
    return db.findById('daily_prices', id);
  },

  // 创建价格
  create(data) {
    return db.insert('daily_prices', data);
  },

  // 更新价格
  update(id, data) {
    return db.update('daily_prices', id, data);
  },

  // 删除价格
  delete(id) {
    db.delete('daily_prices', id);
  },

  // 获取今日价格
  getTodayPrices() {
    const today = new Date().toISOString().split('T')[0];
    return this.findAll({ where: { price_date: today } });
  },

  // 获取最新价格
  getLatestPrices() {
    const products = db.get('products');
    const prices = db.get('daily_prices');

    // 获取每个产品的最新价格
    const latestPrices = [];
    products.forEach(product => {
      const productPrices = prices.filter(p => p.product_id == product.id);
      if (productPrices.length > 0) {
        // 按日期排序取最新
        productPrices.sort((a, b) => new Date(b.price_date) - new Date(a.price_date));
        latestPrices.push({
          ...productPrices[0],
          product
        });
      }
    });

    return latestPrices;
  },

  // 获取历史价格
  getHistory(productId, days = 30) {
    const startDate = new Date();
    startDate.setDate(startDate.getDate() - days);
    const startDateStr = startDate.toISOString().split('T')[0];

    return db.query('daily_prices', {
      where: {
        product_id: productId,
        price_date: { gte: startDateStr }
      },
      orderBy: { price_date: 'asc' }
    });
  },

  // 获取待审核价格
  getPendingPrices() {
    return db.query('daily_prices', { where: { status: 0 } });
  },

  // 审核价格
  verify(id, verifiedBy) {
    return db.update('daily_prices', id, {
      status: 1,
      verified_by: verifiedBy,
      verified_at: new Date().toISOString()
    });
  }
};

// 日统计
const DailyStatistics = {
  findAll(conditions = {}) {
    return db.query('daily_statistics', conditions);
  },

  findByDate(date) {
    return db.findOne('daily_statistics', { stat_date: date });
  },

  create(data) {
    return db.insert('daily_statistics', data);
  },

  update(id, data) {
    return db.update('daily_statistics', id, data);
  }
};

// 价格提醒
const PriceAlert = {
  findAll(conditions = {}) {
    return db.query('price_alerts', conditions);
  },

  create(data) {
    return db.insert('price_alerts', data);
  },

  update(id, data) {
    return db.update('price_alerts', id, data);
  },

  delete(id) {
    db.delete('price_alerts', id);
  }
};

module.exports = {
  Price,
  DailyStatistics,
  PriceAlert
};