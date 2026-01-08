const db = require('../config/database');

// 产品模型
const Product = {
  // 获取所有产品
  findAll(conditions = {}) {
    return db.query('products', conditions);
  },

  // 根据条件查找
  findOne(conditions) {
    return db.findOne('products', conditions);
  },

  // 根据ID查找
  findById(id) {
    return db.findById('products', id);
  },

  // 创建产品
  create(data) {
    const categories = db.get('product_categories');
    const grades = db.get('product_grades');
    const origins = db.get('product_origins');
    const specs = db.get('product_specs');

    const category = categories.find(c => c.id == data.category_id);
    const grade = grades.find(g => g.id == data.grade_id);
    const origin = origins.find(o => o.id == data.origin_id);
    const spec = specs.find(s => s.id == data.spec_id);

    return db.insert('products', {
      ...data,
      category: category ? category.name : '',
      grade: grade ? grade.name : '',
      origin: origin ? origin.name : '',
      spec: spec ? spec.name : ''
    });
  },

  // 更新产品
  update(id, data) {
    return db.update('products', id, data);
  },

  // 删除产品
  delete(id) {
    db.delete('products', id);
  }
};

// 产品类别
const ProductCategory = {
  findAll() {
    return db.query('product_categories', { where: { status: 1 } });
  }
};

// 产品等级
const ProductGrade = {
  findAll() {
    return db.query('product_grades', { where: { status: 1 } });
  }
};

// 产地
const ProductOrigin = {
  findAll() {
    return db.query('product_origins', { where: { status: 1 } });
  }
};

// 规格
const ProductSpec = {
  findAll() {
    return db.query('product_specs', { where: { status: 1 } });
  }
};

module.exports = {
  Product,
  ProductCategory,
  ProductGrade,
  ProductOrigin,
  ProductSpec
};