const fs = require('fs');
const path = require('path');
const crypto = require('crypto');

// 读取环境变量
require('dotenv').config({ path: path.join(__dirname, '../../.env') });

const DATA_DIR = path.join(__dirname, '../../data');
const DB_FILE = path.join(DATA_DIR, 'liupao_price.json');

// 确保数据目录存在
if (!fs.existsSync(DATA_DIR)) {
  fs.mkdirSync(DATA_DIR, { recursive: true });
}

// 简单的JSON数据库
class JsonDB {
  constructor(filename) {
    this.filename = filename;
    this.data = this.load();
  }

  load() {
    try {
      if (fs.existsSync(this.filename)) {
        return JSON.parse(fs.readFileSync(this.filename, 'utf8'));
      }
    } catch (e) {
      console.error('加载数据库失败:', e);
    }
    return {};
  }

  save() {
    fs.writeFileSync(this.filename, JSON.stringify(this.data, null, 2));
  }

  get(collection) {
    if (!this.data[collection]) {
      this.data[collection] = [];
    }
    return this.data[collection];
  }

  set(collection, data) {
    this.data[collection] = data;
    this.save();
  }

  insert(collection, item) {
    const items = this.get(collection);
    item.id = Date.now();
    item.created_at = new Date().toISOString();
    item.updated_at = new Date().toISOString();
    items.push(item);
    this.set(collection, items);
    return item;
  }

  update(collection, id, updates) {
    const items = this.get(collection);
    const index = items.findIndex(item => item.id == id);
    if (index !== -1) {
      items[index] = { ...items[index], ...updates, updated_at: new Date().toISOString() };
      this.set(collection, items);
      return items[index];
    }
    return null;
  }

  delete(collection, id) {
    const items = this.get(collection);
    const filtered = items.filter(item => item.id != id);
    this.set(collection, filtered);
  }

  findById(collection, id) {
    const items = this.get(collection);
    return items.find(item => item.id == id);
  }

  findOne(collection, conditions) {
    const items = this.get(collection);
    return items.find(item => {
      return Object.entries(conditions).every(([key, value]) => item[key] == value);
    });
  }

  findAll(collection, conditions = {}) {
    const items = this.get(collection);
    return items.filter(item => {
      return Object.entries(conditions).every(([key, value]) => {
        if (typeof value === 'function') {
          return value(item[key]);
        }
        return item[key] == value;
      });
    });
  }

  query(collection, conditions = {}) {
    let items = this.get(collection);

    // 筛选
    if (conditions.where) {
      items = items.filter(item => {
        return Object.entries(conditions.where).every(([key, value]) => {
          if (value === undefined) return true;
          if (typeof value === 'object') {
            if (value.like) return String(item[key] || '').includes(value.like);
            if (value.in) return value.in.includes(item[key]);
            if (value.gte) return item[key] >= value.gte;
            if (value.lte) return item[key] <= value.lte;
          }
          return item[key] == value;
        });
      });
    }

    // 排序
    if (conditions.orderBy) {
      const [field, direction] = Object.entries(conditions.orderBy)[0];
      items.sort((a, b) => {
        if (direction === 'desc') {
          return b[field] > a[field] ? 1 : -1;
        }
        return a[field] > b[field] ? 1 : -1;
      });
    }

    // 分页
    if (conditions.limit) {
      const offset = conditions.offset || 0;
      items = items.slice(offset, offset + conditions.limit);
    }

    return items;
  }
}

// 初始化数据库
const db = new JsonDB(DB_FILE);

// 初始化种子数据
function initSeedData() {
  // 产品类别
  if (db.get('product_categories').length === 0) {
    const categories = [
      { id: 1, name: '散茶', code: 'sancha', sort_order: 1, status: 1 },
      { id: 2, name: '紧压茶', code: 'jinmacha', sort_order: 2, status: 1 },
      { id: 3, name: '年份茶', code: 'nianfench', sort_order: 3, status: 1 },
      { id: 4, name: '陈皮普洱', code: 'chenpipu', sort_order: 4, status: 1 }
    ];
    db.set('product_categories', categories);
  }

  // 产品等级
  if (db.get('product_grades').length === 0) {
    const grades = [
      { id: 1, name: '特级', code: 'teji', sort_order: 1, status: 1 },
      { id: 2, name: '一级', code: 'yiji', sort_order: 2, status: 1 },
      { id: 3, name: '二级', code: 'erji', sort_order: 3, status: 1 },
      { id: 4, name: '三级', code: 'sanji', sort_order: 4, status: 1 }
    ];
    db.set('product_grades', grades);
  }

  // 产地
  if (db.get('product_origins').length === 0) {
    const origins = [
      { id: 1, name: '梧州', code: 'wuzhou', region: '梧州产区', status: 1 },
      { id: 2, name: '横州', code: 'hengzhou', region: '横州产区', status: 1 },
      { id: 3, name: '桂林', code: 'guilin', region: '桂林产区', status: 1 },
      { id: 4, name: '柳州', code: 'liuzhou', region: '柳州产区', status: 1 },
      { id: 5, name: '南宁', code: 'nanning', region: '南宁产区', status: 1 }
    ];
    db.set('product_origins', origins);
  }

  // 规格
  if (db.get('product_specs').length === 0) {
    const specs = [
      { id: 1, name: '100g', unit: 'g', weight: 0.1, sort_order: 1, status: 1 },
      { id: 2, name: '250g', unit: 'g', weight: 0.25, sort_order: 2, status: 1 },
      { id: 3, name: '357g', unit: 'g', weight: 0.357, sort_order: 3, status: 1 },
      { id: 4, name: '500g', unit: 'g', weight: 0.5, sort_order: 4, status: 1 },
      { id: 5, name: '1kg', unit: 'kg', weight: 1.0, sort_order: 5, status: 1 },
      { id: 6, name: '10kg', unit: 'kg', weight: 10.0, sort_order: 6, status: 1 },
      { id: 7, name: '一件', unit: '件', weight: 15.0, sort_order: 7, status: 1 }
    ];
    db.set('product_specs', specs);
  }

  // 系统配置
  if (db.get('system_config').length === 0) {
    const configs = [
      { id: 1, key: 'market_name', value: '广西六堡茶大宗交易市场', type: 'string', description: '市场名称' },
      { id: 2, key: 'price_update_time', value: '09:30', type: 'string', description: '价格更新时间' },
      { id: 3, key: 'price_publish_time', value: '10:00', type: 'string', description: '价格发布时间' },
      { id: 4, key: 'timezone', value: 'Asia/Shanghai', type: 'string', description: '时区' },
      { id: 5, key: 'currency', value: 'CNY', type: 'string', description: '货币' }
    ];
    db.set('system_config', configs);
  }

  // 初始用户 (密码: admin123)
  if (db.get('users').length === 0) {
    const bcrypt = require('bcryptjs');
    const hash = bcrypt.hashSync('admin123', 10);
    const users = [
      { id: 1, username: 'admin', password: hash, name: '管理员', role: 'admin', status: 1 },
      { id: 2, username: 'operator', password: hash, name: '操作员', role: 'operator', status: 1 },
      { id: 3, username: 'viewer', password: hash, name: '查看者', role: 'viewer', status: 1 }
    ];
    db.set('users', users);
  }

  // 数据源
  if (db.get('data_sources').length === 0) {
    const sources = [
      { id: 1, name: '人工录入', type: 'manual', status: 1 },
      { id: 2, name: '东和茶仓API', type: 'api', status: 1 },
      { id: 3, name: '茶交所行情', type: 'api', status: 1 }
    ];
    db.set('data_sources', sources);
  }

  // 初始产品示例
  if (db.get('products').length === 0) {
    const products = [
      { id: 1, code: 'LP-2024-001', name: '六堡茶2023年陈', category_id: 1, grade_id: 1, year: 2023, origin_id: 1, spec_id: 5, status: 1 },
      { id: 2, code: 'LP-2024-002', name: '六堡茶2022年陈', category_id: 1, grade_id: 2, year: 2022, origin_id: 1, spec_id: 5, status: 1 },
      { id: 3, code: 'LP-2024-003', name: '六堡茶2021年陈', category_id: 1, grade_id: 2, year: 2021, origin_id: 2, spec_id: 5, status: 1 },
      { id: 4, code: 'LP-2024-004', name: '六堡茶2020年陈', category_id: 3, grade_id: 1, year: 2020, origin_id: 1, spec_id: 5, status: 1 },
      { id: 5, code: 'LP-2024-005', name: '六堡茶2019年陈', category_id: 3, grade_id: 1, year: 2019, origin_id: 1, spec_id: 5, status: 1 }
    ];
    db.set('products', products);
  }

  // 初始价格示例
  if (db.get('daily_prices').length === 0) {
    const today = new Date().toISOString().split('T')[0];
    const prices = [
      { id: 1, product_id: 1, price_date: today, price_buy: 280, price_sell: 320, price_avg: 300, price_change: 10, price_change_percent: 3.45, volume: 5000, turnover: 1500000, status: 1 },
      { id: 2, product_id: 2, price_date: today, price_buy: 380, price_sell: 420, price_avg: 400, price_change: 8, price_change_percent: 2.05, volume: 3200, turnover: 1280000, status: 1 },
      { id: 3, product_id: 3, price_date: today, price_buy: 500, price_sell: 540, price_avg: 520, price_change: 9, price_change_percent: 1.76, volume: 2100, turnover: 1092000, status: 1 },
      { id: 4, product_id: 4, price_date: today, price_buy: 670, price_sell: 690, price_avg: 680, price_change: -3.5, price_change_percent: -0.51, volume: 1500, turnover: 1020000, status: 1 },
      { id: 5, product_id: 5, price_date: today, price_buy: 830, price_sell: 870, price_avg: 850, price_change: 115, price_change_percent: 15.65, volume: 800, turnover: 680000, status: 1 }
    ];
    db.set('daily_prices', prices);
  }

  console.log('✓ 种子数据初始化完成');
}

initSeedData();

module.exports = db;