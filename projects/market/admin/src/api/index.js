import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1';

const request = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// 响应拦截器
request.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API 方法
export const api = {
  // Auth
  login: (data) => request.post('/auth/login', data),
  getMe: () => request.get('/auth/me'),
  
  // Products
  getProducts: (params) => request.get('/products', { params }),
  getProductOptions: () => request.get('/products/options'),
  getProduct: (id) => request.get(`/products/${id}`),
  createProduct: (data) => request.post('/products', data),
  updateProduct: (id, data) => request.put(`/products/${id}`, data),
  deleteProduct: (id) => request.delete(`/products/${id}`),
  
  // Prices
  getPrices: (params) => request.get('/prices', { params }),
  getTodayPrices: () => request.get('/prices/today'),
  getPriceHistory: (productId, params) => request.get(`/prices/${productId}/history`, { params }),
  createPrice: (data) => request.post('/prices', data),
  verifyPrices: (data) => request.post('/prices/verify', data),
  getPendingPrices: () => request.get('/prices/verify/pending'),
  
  // Statistics
  getDailyStats: (params) => request.get('/statistics/daily', { params }),
  getTrend: (params) => request.get('/statistics/trend', { params }),
  getRankings: (params) => request.get('/statistics/rankings', { params }),
  
  // Sources
  getSources: () => request.get('/sources'),
  createSource: (data) => request.post('/sources', data),
  updateSource: (id, data) => request.put(`/sources/${id}`, data),
  deleteSource: (id) => request.delete(`/sources/${id}`),
  
  // System
  getConfig: () => request.get('/system/config'),
  updateConfig: (data) => request.put('/system/config', data),
  getStats: () => request.get('/system/stats')
};

export default api;
