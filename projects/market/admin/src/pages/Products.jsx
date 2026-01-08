import React, { useState, useEffect } from 'react';
import { Table, Card, Button, Space, Tag, message, Modal, Form, Input, Select, InputNumber } from 'antd';
import { PlusOutlined, EditOutlined, DeleteOutlined } from '@ant-design/icons';
import { api } from '../../api';

const Products = () => {
  const [products, setProducts] = useState([]);
  const [options, setOptions] = useState({});
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [editingProduct, setEditingProduct] = useState(null);
  const [pagination, setPagination] = useState({ current: 1, pageSize: 20, total: 0 });

  const [form] = Form.useForm();

  useEffect(() => {
    loadOptions();
    loadProducts();
  }, []);

  const loadOptions = async () => {
    try {
      const res = await api.getProductOptions();
      setOptions(res.data);
    } catch (error) {
      console.error('加载选项失败:', error);
    }
  };

  const loadProducts = async (page = 1) => {
    setLoading(true);
    try {
      const res = await api.getProducts({ page, pageSize: 20 });
      setProducts(res.data.list);
      setPagination({ ...pagination, current: page, total: res.data.pagination.total });
    } catch (error) {
      message.error('加载产品失败');
    } finally {
      setLoading(false);
    }
  };

  const handleAdd = () => {
    setEditingProduct(null);
    form.resetFields();
    setModalVisible(true);
  };

  const handleEdit = (record) => {
    setEditingProduct(record);
    form.setFieldsValue(record);
    setModalVisible(true);
  };

  const handleSubmit = async () => {
    try {
      const values = await form.validateFields();
      if (editingProduct) {
        await api.updateProduct(editingProduct.id, values);
        message.success('更新成功');
      } else {
        await api.createProduct(values);
        message.success('创建成功');
      }
      setModalVisible(false);
      loadProducts(pagination.current);
    } catch (error) {
      message.error('操作失败');
    }
  };

  const handleDelete = async (id) => {
    Modal.confirm({
      title: '确认删除',
      content: '确定要删除这个产品吗？',
      onOk: async () => {
        try {
          await api.deleteProduct(id);
          message.success('删除成功');
          loadProducts(pagination.current);
        } catch (error) {
          message.error('删除失败');
        }
      }
    });
  };

  const columns = [
    { title: '编码', dataIndex: 'code', key: 'code', width: 120 },
    { title: '品名', dataIndex: 'name', key: 'name' },
    { title: '类别', dataIndex: ['category', 'name'], key: 'category', width: 100 },
    { title: '等级', dataIndex: ['grade', 'name'], key: 'grade', width: 80 },
    { title: '年份', dataIndex: 'year', key: 'year', width: 80 },
    { title: '产地', dataIndex: ['origin', 'name'], key: 'origin', width: 80 },
    {
      title: '状态',
      dataIndex: 'status',
      key: 'status',
      width: 80,
      render: (v) => <Tag color={v === 1 ? 'green' : 'red'}>{v === 1 ? '正常' : '停用'}</Tag>
    },
    {
      title: '操作',
      key: 'action',
      width: 150,
      render: (_, record) => (
        <Space>
          <Button type="link" icon={<EditOutlined />} onClick={() => handleEdit(record)}>编辑</Button>
          <Button type="link" danger icon={<DeleteOutlined />} onClick={() => handleDelete(record.id)}>删除</Button>
        </Space>
      )
    }
  ];

  return (
    <Card
      title="产品管理"
      extra={<Button type="primary" icon={<PlusOutlined />} onClick={handleAdd}>新增产品</Button>}
    >
      <Table
        columns={columns}
        dataSource={products}
        loading={loading}
        rowKey="id"
        pagination={pagination}
        onChange={(p) => loadProducts(p.current)}
      />

      <Modal
        title={editingProduct ? '编辑产品' : '新增产品'}
        open={modalVisible}
        onOk={handleSubmit}
        onCancel={() => setModalVisible(false)}
      >
        <Form form={form} layout="vertical">
          <Form.Item name="code" label="产品编码" rules={[{ required: true }]}>
            <Input placeholder="如: LP-2024-001" />
          </Form.Item>
          <Form.Item name="name" label="品名" rules={[{ required: true }]}>
            <Input placeholder="如: 六堡茶2023年陈" />
          </Form.Item>
          <Form.Item name="category_id" label="类别">
            <Select placeholder="选择类别" options={options.categories?.map(c => ({ label: c.name, value: c.id }))} />
          </Form.Item>
          <Form.Item name="grade_id" label="等级">
            <Select placeholder="选择等级" options={options.grades?.map(g => ({ label: g.name, value: g.id }))} />
          </Form.Item>
          <Form.Item name="year" label="年份">
            <InputNumber placeholder="如: 2023" style={{ width: '100%' }} />
          </Form.Item>
          <Form.Item name="origin_id" label="产地">
            <Select placeholder="选择产地" options={options.origins?.map(o => ({ label: o.name, value: o.id }))} />
          </Form.Item>
        </Form>
      </Modal>
    </Card>
  );
};

export default Products;
