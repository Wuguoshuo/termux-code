import React, { useState, useEffect } from 'react';
import { Row, Col, Card, Statistic, Table, Tag } from 'antd';
import { ArrowUpOutlined, ArrowDownOutlined } from '@ant-design/icons';
import ReactECharts from 'echarts-for-react';
import { api } from '../../api';

const Dashboard = () => {
  const [stats, setStats] = useState({});
  const [todayPrices, setTodayPrices] = useState([]);
  const [dailyStats, setDailyStats] = useState(null);

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [statsRes, pricesRes, dailyRes] = await Promise.all([
        api.getStats(),
        api.getTodayPrices(),
        api.getDailyStats({})
      ]);
      setStats(statsRes.data);
      setTodayPrices(pricesRes.data?.prices || []);
      setDailyStats(dailyRes.data);
    } catch (error) {
      console.error('加载数据失败:', error);
    }
  };

  const priceChartOption = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: todayPrices.slice(0, 10).map(p => p.productName?.substring(0, 8))
    },
    yAxis: { type: 'value' },
    series: [{
      data: todayPrices.slice(0, 10).map(p => p.price),
      type: 'line',
      smooth: true,
      itemStyle: { color: '#1890ff' }
    }]
  };

  const columns = [
    { title: '产品', dataIndex: 'productName', key: 'productName', ellipsis: true },
    { 
      title: '均价', 
      dataIndex: 'price', 
      key: 'price',
      render: v => `¥${v?.toFixed(2) || '-'}`
    },
    {
      title: '涨跌',
      dataIndex: 'changePercent',
      key: 'changePercent',
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
      <Row gutter={16} className="dashboard-cards">
        <Col span={6}>
          <Card>
            <Statistic
              title="产品总数"
              value={stats.totalProducts || 0}
              valueStyle={{ color: '#1890ff' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="今日报价"
              value={stats.todayPrices || 0}
              valueStyle={{ color: '#52c41a' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="数据源"
              value={stats.totalSources || 0}
              valueStyle={{ color: '#722ed1' }}
            />
          </Card>
        </Col>
        <Col span={6}>
          <Card>
            <Statistic
              title="上涨品种"
              value={dailyStats?.rising_count || 0}
              valueStyle={{ color: '#ff4d4f' }}
              suffix={`/ ${dailyStats?.total_products || 0}`}
            />
          </Card>
        </Col>
      </Row>

      <Row gutter={16}>
        <Col span={16}>
          <Card title="价格走势">
            <ReactECharts option={priceChartOption} style={{ height: 300 }} />
          </Card>
        </Col>
        <Col span={8}>
          <Card title="今日报价">
            <Table
              columns={columns}
              dataSource={todayPrices.slice(0, 5)}
              rowKey="productId"
              pagination={false}
              size="small"
            />
          </Card>
        </Col>
      </Row>
    </div>
  );
};

export default Dashboard;
