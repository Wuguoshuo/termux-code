import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { Card, Select, Row, Col } from 'antd';
import ReactECharts from 'echarts-for-react';
import axios from 'axios';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:3000/api/v1';

const Trend = () => {
  const [trend, setTrend] = useState([]);
  const [loading, setLoading] = useState(true);
  const [days, setDays] = useState(30);

  useEffect(() => {
    loadTrend();
  }, [days]);

  const loadTrend = async () => {
    setLoading(true);
    try {
      const endDate = new Date().toISOString().split('T')[0];
      const startDate = new Date();
      startDate.setDate(startDate.getDate() - days);
      
      const res = await axios.get(`${API_URL}/statistics/trend`, {
        params: { startDate: startDate.toISOString().split('T')[0], endDate }
      });
      setTrend(res.data.data?.trend || []);
    } catch (error) {
      console.error('加载趋势数据失败:', error);
    } finally {
      setLoading(false);
    }
  };

  const priceChartOption = {
    tooltip: { trigger: 'axis' },
    legend: { data: ['均价', '成交量'] },
    xAxis: {
      type: 'category',
      data: trend.map(t => t.date)
    },
    yAxis: [
      { type: 'value', name: '均价(元)', position: 'left' },
      { type: 'value', name: '成交量', position: 'right' }
    ],
    series: [
      {
        name: '均价',
        type: 'line',
        data: trend.map(t => t.avgPrice),
        smooth: true,
        itemStyle: { color: '#1890ff' }
      },
      {
        name: '成交量',
        type: 'bar',
        yAxisIndex: 1,
        data: trend.map(t => t.volume),
        itemStyle: { color: '#52c41a' }
      }
    ]
  };

  const volumeChartOption = {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: trend.map(t => t.date)
    },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: trend.map(t => t.turnover),
      itemStyle: { color: '#722ed1' }
    }]
  };

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
        <Card
          title="价格走势分析"
          extra={
            <Select value={days} onChange={setDays} style={{ width: 120 }}>
              <Select.Option value={7}>近7天</Select.Option>
              <Select.Option value={30}>近30天</Select.Option>
              <Select.Option value={90}>近90天</Select.Option>
            </Select>
          }
        >
          <Row gutter={16}>
            <Col span={16}>
              <ReactECharts option={priceChartOption} style={{ height: 400 }} />
            </Col>
            <Col span={8}>
              <ReactECharts option={volumeChartOption} style={{ height: 400 }} />
            </Col>
          </Row>
        </Card>
      </div>
    </div>
  );
};

export default Trend;
