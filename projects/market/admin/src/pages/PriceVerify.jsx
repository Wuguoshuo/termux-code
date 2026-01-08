import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Tag, message, Modal } from 'antd';
import { CheckOutlined, CloseOutlined } from '@ant-design/icons';
import { api } from '../../api';

const PriceVerify = () => {
  const [prices, setPrices] = useState([]);
  const [loading, setLoading] = useState(false);

  const loadPrices = async () => {
    setLoading(true);
    try {
      const res = await api.getPendingPrices();
      setPrices(res.data || []);
    } catch (error) {
      message.error('加载待审核数据失败');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadPrices();
  }, []);

  const handleVerify = async (ids, action) => {
    try {
      await api.verifyPrices({ ids, action });
      message.success(action === 'approve' ? '审核通过' : '已驳回');
      loadPrices();
    } catch (error) {
      message.error('操作失败');
    }
  };

  const columns = [
    { title: '产品', dataIndex: ['product', 'name'], key: 'product' },
    { title: '日期', dataIndex: 'price_date', key: 'date', width: 120 },
    { title: '买入价', dataIndex: 'price_buy', key: 'buy', width: 100, render: v => `¥${v || '-'}` },
    { title: '卖出价', dataIndex: 'price_sell', key: 'sell', width: 100, render: v => `¥${v || '-'}` },
    { title: '均价', dataIndex: 'price_avg', key: 'avg', width: 100, render: v => `¥${v || '-'}` },
    { title: '来源', dataIndex: 'source_type', key: 'source', width: 80, render: v => <Tag>{v}</Tag> },
    { title: '录入时间', dataIndex: 'created_at', key: 'created', width: 160 },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button type="primary" size="small" icon={<CheckOutlined />} onClick={() => handleVerify([record.id], 'approve')}>通过</Button>
          <Button danger size="small" icon={<CloseOutlined />} onClick={() => handleVerify([record.id], 'reject')}>驳回</Button>
        </Space>
      )
    }
  ];

  return (
    <Card
      title="价格审核"
      extra={<Button onClick={loadPrices}>刷新</Button>}
    >
      <Table
        columns={columns}
        dataSource={prices}
        loading={loading}
        rowKey="id"
        pagination={{ pageSize: 10 }}
        rowSelection={{
          onChange: (selectedRowKeys) => {
            window.selectedIds = selectedRowKeys;
          }
        }}
      />
      {prices.length > 0 && (
        <div style={{ marginTop: 16 }}>
          <Space>
            <Button type="primary" onClick={() => handleVerify(window.selectedIds || [], 'approve')}>批量通过</Button>
            <Button onClick={() => handleVerify(window.selectedIds || [], 'reject')}>批量驳回</Button>
          </Space>
        </div>
      )}
    </Card>
  );
};

export default PriceVerify;
