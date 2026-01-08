const { Product, ProductCategory, ProductGrade, ProductOrigin, ProductSpec } = require('./product');
const { Price, DailyStatistics, PriceAlert } = require('./price');
const { User, OperationLog } = require('./user');

module.exports = {
  Product,
  ProductCategory,
  ProductGrade,
  ProductOrigin,
  ProductSpec,
  Price,
  DailyStatistics,
  PriceAlert,
  User,
  OperationLog
};