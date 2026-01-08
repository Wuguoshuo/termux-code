import React, { useState, useEffect } from 'react';
import { Menu } from 'antd';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  DashboardOutlined,
  AppstoreOutlined,
  DollarOutlined,
  CheckCircleOutlined,
  CloudOutlined,
  SettingOutlined
} from '@ant-design/icons';

const SiderMenu = () => {
  const navigate = useNavigate();
  const location = useLocation();
  
  const menuItems = [
    {
      key: '/dashboard',
      icon: <DashboardOutlined />,
      label: '仪表盘'
    },
    {
      key: '/products',
      icon: <AppstoreOutlined />,
      label: '产品管理'
    },
    {
      key: '/prices',
      icon: <DollarOutlined />,
      label: '报价管理'
    },
    {
      key: '/prices/verify',
      icon: <CheckCircleOutlined />,
      label: '价格审核'
    },
    {
      key: '/sources',
      icon: <CloudOutlined />,
      label: '数据源'
    },
    {
      key: '/settings',
      icon: <SettingOutlined />,
      label: '系统设置'
    }
  ];

  return (
    <Menu
      theme="dark"
      mode="inline"
      selectedKeys={[location.pathname]}
      items={menuItems}
      onClick={({ key }) => navigate(key)}
    />
  );
};

export default SiderMenu;
