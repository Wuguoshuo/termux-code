const db = require('../src/config/database');

console.log('数据库初始化检查...');

// 检查各表数据
console.log('产品类别:', db.get('product_categories').length, '条');
console.log('产品等级:', db.get('product_grades').length, '条');
console.log('产地:', db.get('product_origins').length, '条');
console.log('规格:', db.get('product_specs').length, '条');
console.log('产品:', db.get('products').length, '条');
console.log('价格:', db.get('daily_prices').length, '条');
console.log('用户:', db.get('users').length, '条');
console.log('系统配置:', db.get('system_config').length, '条');

console.log('\n✓ 数据库初始化完成！');
console.log('默认账号: admin / admin123');