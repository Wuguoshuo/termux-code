import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Table, Tag, Select, Input } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1';

const Prices = () => {
  const [prices, setPrices] = useState([]);
  const [options, setOptions] = useState({});
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState({});

  useEffect(() => {
    loadOptions();
    loadPrices();
  }, []);

  const loadOptions = async () => {
    try {
      const res = await axios.get(`${API_URL}/products/options`);
      setOptions(res.data.data);
    } catch (error) {
      console.error('加载选项失败:', error);
    }
  };

  const loadPrices = async (params = {}) => {
    setLoading(true);
    try {
      const res = await axios.get(`${API_URL}/prices`, { params: { ...params, pageSize: 50 } });
      setPrices(res.data.data?.list || []);
    } catch (error) {
      console.error('加载价格失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleFilter = (key, value) => {
    const newFilters = { ...filters, [key]: value };
    setFilters(newFilters);
    loadPrices(newFilters);
  };

  const columns = [
    { title: '产品', dataIndex: ['product', 'name'], key: 'name', width: 200 },
    { title: '类别', dataIndex: ['product', 'category', 'name'], key: 'category', width: 100 },
    { title: '等级', dataIndex: ['product', 'grade', 'name'], key: 'grade', width: 80 },
    { title: '年份', dataIndex: ['product', 'year'], key: 'year', width: 80 },
    {
      title: '买入价',
      dataIndex: 'price_buy',
      key: 'buy',
      width: 100,
      render: v => v ? `¥${v.toFixed(2)}` : '-'
    },
    {
      title: '卖出价',
      dataIndex: 'price_sell',
      key: 'sell',
      width: 100,
      render: v => v ? `¥${v.toFixed(2)}` : '-'
    },
    {
      title: '均价',
      dataIndex: 'price_avg',
      key: 'avg',
      width: 100,
      render: v => v ? `¥${v.toFixed(2)}` : '-'
    },
    {
      title: '涨跌',
      dataIndex: 'price_change_percent',
      key: 'change',
      width: 100,
      render: (v) => (
        <Tag color={v > 0 ? 'red' : v < 0 ? 'green' : 'default'}>
          {v > 0 ? <ArrowUpOutlined /> : v < 0 ? <ArrowDownOutlined /> : null}
          {v > 0 ? '+' : ''}{v?.toFixed(2) || 0}%
        </Tag>
      )
    },
    {
      title: '成交量',
      dataIndex: 'volume',
      key: 'volume',
      width: 120,
      render: v => v?.toLocaleString() || '-'
    }
  ];

  return (
    <div>
      <header className="header">
        <div className="logo">🏭 广西六堡茶大宗交易市场</div>
        <nav className="nav">
          <Link to="/">首页</Link>
          <Link to="/prices">今日报价</Link>
          <Link to="/trend">价格走势</Link>
        </nav>
      </header>

      <div className="container">
        <Card title="大宗单品报价">
          <div className="search-bar">
            <Select
              placeholder="品类"
              allowClear
              style={{ width: 120 }}
              options={options.categories?.map(c => ({ label: c.name, value: c.id }))}
              onChange={(v) => handleFilter('categoryId', v)}
            />
            <Select
              placeholder="等级"
              allowClear
              style={{ width: 100 }}
              options={options.grades?.map(g => ({ label: g.name, value: g.id }))}
              onChange={(v) => handleFilter('gradeId', v)}
            />
            <Select
              placeholder="年份"
              allowClear
              style={{ width: 100 }}
              options={[2024,2023,2022,2021,2020,2019,2018].map(y => ({ label: y, value: y }))}
              onChange={(v) => handleFilter('year', v)}
            />
            <Input.Search
              placeholder="搜索品名"
              style={{ width: 200 }}
              onSearch={(v) => handleFilter('keyword', v)}
            />
          </div>

          <Table
            columns={columns}
            dataSource={prices}
            loading={loading}
            rowKey="id"
            pagination={{ pageSize: 20 }}
          />
        </Card>
      </div>
    </div>
  );
};

export default Prices;
