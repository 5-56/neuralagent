/**
 * 羲和应用主布局组件
 */

import React, { useState } from 'react';
import { Outlet } from 'react-router-dom';
import styled from 'styled-components';
import { motion } from 'framer-motion';

// 组件
import Sidebar from './Sidebar';
import Header from './Header';
import StatusBar from './StatusBar';

// 样式
const LayoutContainer = styled.div`
  display: flex;
  height: 100vh;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text};
  overflow: hidden;
`;

const MainContent = styled(motion.div)`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
`;

const ContentArea = styled.div`
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
`;

const PageContainer = styled(motion.div)`
  flex: 1;
  padding: 24px;
  overflow-y: auto;
  overflow-x: hidden;
  
  &::-webkit-scrollbar {
    width: 8px;
  }
  
  &::-webkit-scrollbar-track {
    background: ${props => props.theme.colors.backgroundSecondary};
  }
  
  &::-webkit-scrollbar-thumb {
    background: ${props => props.theme.colors.border};
    border-radius: 4px;
  }
  
  &::-webkit-scrollbar-thumb:hover {
    background: ${props => props.theme.colors.textSecondary};
  }
`;

const Layout = () => {
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  const [isOverlayVisible, setIsOverlayVisible] = useState(false);

  const toggleSidebar = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const toggleOverlay = () => {
    setIsOverlayVisible(!isOverlayVisible);
    // 通知Electron主进程
    window.electronAPI?.toggleOverlay();
  };

  return (
    <LayoutContainer>
      {/* 侧边栏 */}
      <Sidebar 
        collapsed={sidebarCollapsed}
        onToggle={toggleSidebar}
      />
      
      {/* 主内容区域 */}
      <MainContent
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.3 }}
      >
        {/* 头部 */}
        <Header 
          onToggleSidebar={toggleSidebar}
          onToggleOverlay={toggleOverlay}
          isOverlayVisible={isOverlayVisible}
        />
        
        {/* 内容区域 */}
        <ContentArea>
          <PageContainer
            initial={{ y: 20, opacity: 0 }}
            animate={{ y: 0, opacity: 1 }}
            transition={{ duration: 0.3, delay: 0.1 }}
          >
            <Outlet />
          </PageContainer>
        </ContentArea>
        
        {/* 状态栏 */}
        <StatusBar />
      </MainContent>
    </LayoutContainer>
  );
};

export default Layout;