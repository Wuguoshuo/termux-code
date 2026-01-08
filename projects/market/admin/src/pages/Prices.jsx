import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Tag, DatePicker, Select, message, Modal, Form, InputNumber } from 'antd';
import { PlusOutlined, CheckOutlined, CloseOutlined } from '@ant-design/icons';
import dayjs from 'dayjs';
import { api } from '../../api';

const { RangePicker } = DatePicker;

const Prices = () => {
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(false);
  const [options, setOptions] = useState({});
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });
  const [filters, setFilters] = useState({});
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    loadOptions();
    loadPrices();
  }, []);

  const loadOptions = async () => {
    try {
      const res = await api.getProductOptions();
      setOptions(res.data);
    } catch (error) {
      console.error('加载选项失败:', error);
    }
  };

  const loadPrices = async (page = 1, params = {}) => {
    setLoading(true);
    try {
      const res = await api.getPrices({ ...params, page, pageSize: 20 });
      setPrices(res.data.list);
      setPagination({ ...pagination, current: page, total: res.data.pagination.total });
    } catch (error) {
      message.error('加载价格失败');
    } finally {
      setLoading(false);
    }
  };

  const handleSearch = (values) => {
    const params = {};
    if (values.date) params.date = values.date.format('YYYY-MM-DD');
    if (values.categoryId) params.categoryId = values.categoryId;
    if (values.gradeId) params.gradeId = values.gradeId;
    if (values.year) params.year = values.year;
    setFilters(params);
    loadPrices(1, params);
  };

  const handleAdd = () => {
    form.resetFields();
    setModalVisible(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await api.createPrice(values);
      message.success('录入成功');
      setModalVisible(false);
      loadPrices(pagination.current, filters);
    } catch (error) {
      message.error('录入失败');
    }
  };

  const columns = [
    { title: '产品', dataIndex: ['product', 'name'], key: 'product', ellipsis: true },
    { title: '日期', dataIndex: 'price_date', key: 'date', width: 120 },
    { title: '买入价', dataIndex: 'price_buy', key: 'buy', width: 100, render: v => `¥${v || '-'}` },
    { title: '卖出价', dataIndex: 'price_sell', key: 'sell', width: 100, render: v => `¥${v || '-'}` },
    { title: '均价', dataIndex: 'price_avg', key: 'avg', width: 100, render: v => `¥${v || '-'}` },
    {
      title: '涨跌',
      dataIndex: 'price_change_percent',
      key: 'change',
      width: 100,
      render: (v) => (
        <Tag color={v > 0 ? 'red' : v < 0 ? 'green' : 'default'}>
          {v > 0 ? '+' : ''}{v?.toFixed(2) || 0}%
        </Tag>
      )
    },
    { title: '成交量', dataIndex: 'volume', key: 'volume', width: 120, render: v => v?.toLocaleString() || '-' },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (v) => (
        <Tag color={v === 1 ? 'green' : v === 0 ? 'orange' : 'red'}>
          {v === 1 ? '已发布' : v === 0 ? '待审核' : '已驳回'}
        </Tag>
      )
    }
  ];

  return (
    <Card
      title="报价管理"
      extra={
        <Space>
          <Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>录入报价</Button>
        </Space>
      }
    >
      <Form layout="inline" style={{ marginBottom: 16 }} onFinish={handleSearch}>
        <Form.Item name="date">
          <DatePicker placeholder="选择日期" />
        </Form.Item>
        <Form.Item name="categoryId">
          <Select placeholder="品类" style={{ width: 120 }} allowClear options={options.categories?.map(c => ({ label: c.name, value: c.id }))} />
        </Form.Item>
        <Form.Item name="gradeId">
          <Select placeholder="等级" style={{ width: 100 }} allowClear options={options.grades?.map(g => ({ label: g.name, value: g.id }))} />
        </Form.Item>
        <Form.Item name="year">
          <InputNumber placeholder="年份" style={{ width: 100 }} />
        </Form.Item>
        <Form.Item>
          <Button type="primary" htmlType="submit">查询</Button>
        </Form.Item>
      </Form>

      <Table
        columns={columns}
        dataSource={prices}
        loading={loading}
        rowKey="id"
        pagination={pagination}
        onChange={(p) => loadPrices(p.current, filters)}
      />

      <Modal title="录入报价" open={modalVisible} onOk={handleSubmit} onCancel={() => setModalVisible(false)}>
        <Form form={form} layout="vertical">
          <Form.Item name="product_id" label="产品" rules={[{ required: true }]}>
            <Select
              placeholder="选择产品"
              showSearch
              optionFilterProp="label"
              options={prices.map(p => ({ label: p.product?.name, value: p.product?.id }))}
            />
          </Form.Item>
          <Form.Item name="price_date" label="日期" rules={[{ required: true }]}>
            <DatePicker style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="price_buy" label="买入价">
            <InputNumber prefix="¥" style={{ width: '100%' }} precision={2} />
          </Form.Item>
          <Form.Item name="price_sell" label="卖出价">
            <InputNumber prefix="¥" style={{ width: '100%' }} precision={2} />
          </Form.Item>
          <Form.Item name="price_avg" label="均价">
            <InputNumber prefix="¥" style={{ width: '100%' }} precision={2} />
          </Form.Item>
          <Form.Item name="volume" label="成交量">
            <InputNumber style={{ width: '100%' }} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Prices;
