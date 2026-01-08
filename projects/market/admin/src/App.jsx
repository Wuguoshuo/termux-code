import React from 'react';
import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from 'antd';
import SiderMenu from './components/Layout/SiderMenu';
import HeaderBar from './components/Layout/HeaderBar';
import Dashboard from './pages/Dashboard';
import Products from './pages/Products';
import Prices from './pages/Prices';
import PriceVerify from './pages/PriceVerify';
import Sources from './pages/Sources';
import Settings from './pages/Settings';
import Login from './pages/Login';
import './App.css';

const { Header, Content, Sider } = Layout;

function App() {
  const token = localStorage.getItem('token');
  
  if (!token) {
    return <Login />;
  }

  return (
    <Layout style={{ minHeight: '100vh' }}>
      <Sider width={220} theme="dark">
        <div className="logo">六堡茶价格系统</div>
        <SiderMenu />
      </Sider>
      <Layout>
        <Header style={{ padding: '0 24px', background: '#fff', display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <span style={{ fontSize: 18, fontWeight: 'bold' }}>管理后台</span>
          <HeaderBar />
        </Header>
        <Content style={{ margin: '16px' }}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/products" element={<Products />} />
            <Route path="/prices" element={<Prices />} />
            <Route path="/prices/verify" element={<PriceVerify />} />
            <Route path="/sources" element={<Sources />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Content>
      </Layout>
    </Layout>
  );
}

export default App;
