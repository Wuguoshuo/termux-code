import React, { useState, useEffect } from 'react';
import { Card, Form, Input, Button, message, Row, Col } from 'antd';
import { api } from '../../api';

const Settings = () => {
  const [loading, setLoading] = useState(false);
  const [form] = Form.useForm();

  useEffect(() => {
    loadConfig();
  }, []);

  const loadConfig = async () => {
    try {
      const res = await api.getConfig();
      form.setFieldsValue(res.data);
    } catch (error) {
      message.error('加载配置失败');
    }
  };

  const handleSubmit = async () => {
    try {
      const values = form.getFieldsValue();
      for (const [key, value] of Object.entries(values)) {
        await api.updateConfig({ key, value: String(value) });
      }
      message.success('配置保存成功');
    } catch (error) {
      message.error('保存失败');
    }
  };

  return (
    <Card title="系统设置">
      <Form form={form} layout="vertical" style={{ maxWidth: 600 }}>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item name="market_name" label="市场名称">
              <Input placeholder="广西六堡茶大宗交易市场" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="price_update_time" label="价格更新时间">
              <Input placeholder="09:30" />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item name="price_publish_time" label="价格发布时间">
              <Input placeholder="10:00" />
            </Form.Item>
          </Col>
          <Col span={12}>
            <Form.Item name="timezone" label="时区">
              <Input placeholder="Asia/Shanghai" />
            </Form.Item>
          </Col>
        </Row>
        <Row gutter={16}>
          <Col span={12}>
            <Form.Item name="currency" label="货币">
              <Input placeholder="CNY" />
            </Form.Item>
          </Col>
        </Row>
        <Form.Item>
          <Button type="primary" onClick={handleSubmit} loading={loading}>保存配置</Button>
        </Form.Item>
      </Form>
    </Card>
  );
};

export default Settings;
