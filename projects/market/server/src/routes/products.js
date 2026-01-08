const express = require('express');
const { Product, ProductCategory, ProductGrade, ProductOrigin, ProductSpec } = require('../models');
const { auth, verifyRole } = require('../middleware/auth');
const { success, fail } = require('../utils/response');

const router = express.Router();

// 获取产品类别
router.get('/categories', (req, res) => {
  try {
    const categories = ProductCategory.findAll();
    success(res, categories);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取产品等级
router.get('/grades', (req, res) => {
  try {
    const grades = ProductGrade.findAll();
    success(res, grades);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取产地
router.get('/origins', (req, res) => {
  try {
    const origins = ProductOrigin.findAll();
    success(res, origins);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取规格
router.get('/specs', (req, res) => {
  try {
    const specs = ProductSpec.findAll();
    success(res, specs);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取产品列表
router.get('/', (req, res) => {
  try {
    const { category_id, grade_id, origin_id, year, keyword, status = 1 } = req.query;

    const conditions = { where: {} };
    if (status) conditions.where.status = parseInt(status);
    if (category_id) conditions.where.category_id = parseInt(category_id);
    if (grade_id) conditions.where.grade_id = parseInt(grade_id);
    if (origin_id) conditions.where.origin_id = parseInt(origin_id);
    if (year) conditions.where.year = parseInt(year);
    if (keyword) conditions.where.name = { like: keyword };

    const products = Product.findAll(conditions);
    success(res, products);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 获取产品详情
router.get('/:id', (req, res) => {
  try {
    const product = Product.findById(req.params.id);
    if (!product) {
      return fail(res, '产品不存在', 404);
    }
    success(res, product);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 创建产品
router.post('/', auth, verifyRole(['admin', 'operator']), (req, res) => {
  try {
    const { code, name, category_id, grade_id, year, origin_id, spec_id, brand_id, storage_type, description } = req.body;

    if (!code || !name) {
      return fail(res, '产品编码和名称不能为空', 400);
    }

    // 检查编码是否已存在
    const existing = Product.findOne({ code });
    if (existing) {
      return fail(res, '产品编码已存在', 400);
    }

    const product = Product.create({
      code,
      name,
      category_id: parseInt(category_id) || null,
      grade_id: parseInt(grade_id) || null,
      year: parseInt(year) || null,
      origin_id: parseInt(origin_id) || null,
      spec_id: parseInt(spec_id) || null,
      brand_id: parseInt(brand_id) || null,
      storage_type,
      description,
      status: 1
    });

    success(res, product, '创建成功', 201);
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 更新产品
router.put('/:id', auth, verifyRole(['admin', 'operator']), (req, res) => {
  try {
    const product = Product.findById(req.params.id);
    if (!product) {
      return fail(res, '产品不存在', 404);
    }

    Product.update(req.params.id, req.body);
    const updated = Product.findById(req.params.id);
    success(res, updated, '更新成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

// 删除产品
router.delete('/:id', auth, verifyRole(['admin']), (req, res) => {
  try {
    const product = Product.findById(req.params.id);
    if (!product) {
      return fail(res, '产品不存在', 404);
    }

    Product.delete(req.params.id);
    success(res, null, '删除成功');
  } catch (error) {
    fail(res, error.message, 500);
  }
});

module.exports = router;