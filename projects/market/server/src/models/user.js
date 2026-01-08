const db = require('../config/database');

// 用户模型
const User = {
  // 获取所有用户
  findAll(conditions = {}) {
    return db.query('users', conditions);
  },

  // 根据条件查找
  findOne(conditions) {
    return db.findOne('users', conditions);
  },

  // 根据ID查找
  findById(id) {
    return db.findById('users', id);
  },

  // 创建用户
  create(data) {
    return db.insert('users', data);
  },

  // 更新用户
  update(id, data) {
    return db.update('users', id, data);
  },

  // 删除用户
  delete(id) {
    db.delete('users', id);
  }
};

// 操作日志
const OperationLog = {
  create(data) {
    return db.insert('operation_logs', data);
  },

  findAll(conditions = {}) {
    return db.query('operation_logs', conditions);
  }
};

module.exports = {
  User,
  OperationLog
};