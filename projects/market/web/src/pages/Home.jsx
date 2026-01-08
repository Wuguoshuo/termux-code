import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Row, Col, Card, Statistic, Table, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1';

const Home = () => {
  const [stats, setStats] = useState(null);
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, pricesRes] = await Promise.all([
        axios.get(`${API_URL}/statistics/daily`),
        axios.get(`${API_URL}/prices/today`)
      ]);
      setStats(statsRes.data.data);
      setPrices(pricesRes.data.data?.prices || []);
    } catch (error) {
      console.error('加载数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const chartOption = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: prices.slice(0, 10).map(p => p.productName?.substring(0, 8))
    },
    yAxis: { type: 'value' },
    series: [{
      data: prices.slice(0, 10).map(p => p.price),
      type: 'line',
      smooth: true,
      itemStyle: { color: '#1890ff' }
    }]
  };

  const columns = [
    { title: '产品', dataIndex: 'productName', key: 'name', ellipsis: true },
    {
      title: '均价',
      dataIndex: 'price',
      key: 'price',
      render: v => `¥${v?.toFixed(2) || '-'}`
    },
    {
      title: '涨跌',
      dataIndex: 'changePercent',
      key: 'change',
      render: (v) => (
        <Tag color={v > 0 ? 'red' : v < 0 ? 'green' : 'default'}>
          {v > 0 ? <ArrowUpOutlined /> : v < 0 ? <ArrowDownOutlined /> : null}
          {Math.abs(v || 0).toFixed(2)}%
        </Tag>
      )
    },
    {
      title: '成交量',
      dataIndex: 'volume',
      key: 'volume',
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
        <Row gutter={16} className="overview-cards">
          <Col span={6}>
            <Card>
              <Statistic title="报价品种" value={stats?.total_products || 0} valueStyle={{ color: '#1890ff' }} />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="上涨"
                value={stats?.rising_count || 0}
                valueStyle={{ color: '#ff4d4f' }}
                suffix={`/ ${stats?.total_products || 0}`}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="下跌"
                value={stats?.falling_count || 0}
                valueStyle={{ color: '#52c41a' }}
              />
            </Card>
          </Col>
          <Col span={6}>
            <Card>
              <Statistic
                title="整体均价"
                value={stats?.avg_price || 0}
                prefix="¥"
                valueStyle={{ color: '#722ed1' }}
              />
            </Card>
          </Col>
        </Row>

        <Row gutter={16}>
          <Col span={16}>
            <Card title="价格走势">
              <ReactECharts option={chartOption} style={{ height: 300 }} />
            </Card>
          </Col>
          <Col span={8}>
            <Card title="今日报价 TOP10">
              <Table
                columns={columns}
                dataSource={prices.slice(0, 10)}
                rowKey="productId"
                pagination={false}
                size="small"
              />
            </Card>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default Home;
