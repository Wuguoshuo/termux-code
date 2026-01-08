/**
 * API路由入口
 */

const express = require('express');
const router = express.Router();

// 导入各模块路由
const authRoutes = require('./auth');
const productRoutes = require('./products');
const priceRoutes = require('./prices');
const statisticsRoutes = require('./statistics');
const sourceRoutes = require('./sources');
const systemRoutes = require('./system');

// 使用路由
router.use('/auth', authRoutes);
router.use('/products', productRoutes);
router.use('/prices', priceRoutes);
router.use('/statistics', statisticsRoutes);
router.use('/sources', sourceRoutes);
router.use('/system', systemRoutes);

module.exports = router;
