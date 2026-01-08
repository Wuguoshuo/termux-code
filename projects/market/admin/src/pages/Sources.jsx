import React, { useState, useEffect } from 'react';
import { Card, Table, Button, Space, Tag, message, Modal, Form, Input, Select, InputNumber, Switch } from 'antd';
import { PlusOutlined, PlayCircleOutlined } from '@ant-design/icons';
import { api } from '../../api';

const Sources = () => {
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    loadSources();
  }, []);

  const loadSources = async () => {
    setLoading(true);
    try {
      const res = await api.getSources();
      setSources(res.data || []);
    } catch (error) {
      message.error('加载数据源失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    form.resetFields();
    setModalVisible(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      await api.createSource(values);
      message.success('创建成功');
      setModalVisible(false);
      loadSources();
    } catch (error) {
      message.error('创建失败');
    }
  };

  const handleSync = async (id) => {
    try {
      await api.updateSource(id, { status: 1 });
      message.success('同步任务已启动');
    } catch (error) {
      message.error('启动失败');
    }
  };

  const columns = [
    { title: '名称', dataIndex: 'name', key: 'name' },
    { title: '类型', dataIndex: 'type', key: 'type', width: 100, render: v => <Tag>{v}</Tag> },
    { title: 'API地址', dataIndex: 'api_url', key: 'api_url', ellipsis: true },
    { title: '调度', dataIndex: 'crawl_schedule', key: 'schedule', width: 120 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (v) => <Switch checked={v === 1} size="small" />
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button size="small" icon={<PlayCircleOutlined />} onClick={() => handleSync(record.id)}>同步</Button>
        </Space>
      )
    }
  ];

  return (
    <Card
      title="数据源管理"
      extra={<Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增数据源</Button>}
    >
      <Table columns={columns} dataSource={sources} loading={loading} rowKey="id" />

      <Modal title="新增数据源" open={modalVisible} onOk={handleSubmit} onCancel={() => setModalVisible(false)}>
        <Form form={form} layout="vertical">
          <Form.Item name="name" label="名称" rules={[{ required: true }]}>
            <Input placeholder="数据源名称" />
          </Form.Item>
          <Form.Item name="type" label="类型" rules={[{ required: true }]}>
            <Select placeholder="选择类型" options={[
              { label: 'API', value: 'api' },
              { label: '爬虫', value: 'crawler' },
              { label: '手动', value: 'manual' }
            ]} />
          </Form.Item>
          <Form.Item name="api_url" label="API地址">
            <Input placeholder="http://..." />
          </Form.Item>
          <Form.Item name="api_key" label="API密钥">
            <Input.Password placeholder="API密钥" />
          </Form.Item>
          <Form.Item name="crawl_schedule" label="调度周期">
            <Select placeholder="选择调度周期" options={[
              { label: '每小时', value: '0 * * * *' },
              { label: '每天9点', value: '0 9 * * *' },
              { label: '每天2次', value: '0 9,14 * * *' }
            ]} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Sources;
