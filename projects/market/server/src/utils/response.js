/**
 * 统一响应封装
 */

// 成功响应
const success = (res, data = null, message = 'success', code = 200) => {
  res.json({
    code,
    message,
    data
  });
};

// 列表响应(带分页)
const list = (res, list, pagination, message = 'success') => {
  res.json({
    code: 200,
    message,
    data: {
      list,
      pagination
    }
  });
};

// 失败响应
const fail = (res, message = 'error', code = 500, data = null) => {
  res.json({
    code,
    message,
    data
  });
};

module.exports = {
  success,
  list,
  fail
};