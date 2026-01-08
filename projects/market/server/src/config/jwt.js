/**
 * JWT配置
 */

module.exports = {
  secret: process.env.JWT_SECRET || 'liupao-price-secret-key-2024',
  expiresIn: process.env.JWT_EXPIRES_IN || '24h',
  refreshExpiresIn: process.env.JWT_REFRESH_EXPIRES_IN || '7d'
};
