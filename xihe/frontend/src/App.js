/**
 * 羲和桌面应用 - React主应用组件
 */

import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';
import { AnimatePresence } from 'framer-motion';

// 状态管理
import { store } from './store';
import { useAppStore } from './store/useAppStore';

// 组件
import Layout from './components/Layout';
import LoadingScreen from './components/LoadingScreen';
import ErrorBoundary from './components/ErrorBoundary';

// 页面
import HomePage from './pages/HomePage';
import ChatPage from './pages/ChatPage';
import TasksPage from './pages/TasksPage';
import SettingsPage from './pages/SettingsPage';
import OverlayPage from './pages/OverlayPage';

// 样式
import './styles/globals.css';

// 创建React Query客户端
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 3,
      staleTime: 5 * 60 * 1000, // 5分钟
      cacheTime: 10 * 60 * 1000, // 10分钟
    },
  },
});

/**
 * 主应用组件
 */
function App() {
  const { 
    isInitialized, 
    isDarkMode, 
    initializeApp,
    setTheme 
  } = useAppStore();

  useEffect(() => {
    // 初始化应用
    initializeApp();
    
    // 监听系统主题变化
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
    const handleThemeChange = (e) => {
      setTheme(e.matches ? 'dark' : 'light');
    };
    
    mediaQuery.addEventListener('change', handleThemeChange);
    
    return () => {
      mediaQuery.removeEventListener('change', handleThemeChange);
    };
  }, [initializeApp, setTheme]);

  // 应用主题
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', isDarkMode ? 'dark' : 'light');
  }, [isDarkMode]);

  if (!isInitialized) {
    return <LoadingScreen />;
  }

  return (
    <ErrorBoundary>
      <QueryClientProvider client={queryClient}>
        <Router>
          <div className="app">
            <AnimatePresence mode="wait">
              <Routes>
                {/* 主应用路由 */}
                <Route path="/" element={<Layout />}>
                  <Route index element={<HomePage />} />
                  <Route path="chat" element={<ChatPage />} />
                  <Route path="tasks" element={<TasksPage />} />
                  <Route path="settings" element={<SettingsPage />} />
                </Route>
                
                {/* 悬浮窗路由 */}
                <Route path="/overlay" element={<OverlayPage />} />
                
                {/* 重定向 */}
                <Route path="*" element={<Navigate to="/" replace />} />
              </Routes>
            </AnimatePresence>
            
            {/* 全局通知 */}
            <Toaster
              position="top-right"
              toastOptions={{
                duration: 4000,
                style: {
                  background: isDarkMode ? '#1a1a1a' : '#ffffff',
                  color: isDarkMode ? '#ffffff' : '#000000',
                  border: `1px solid ${isDarkMode ? '#333333' : '#e0e0e0'}`,
                },
              }}
            />
          </div>
        </Router>
      </QueryClientProvider>
    </ErrorBoundary>
  );
}

/**
 * 应用入口
 */
function AppWithProvider() {
  return (
    <Provider store={store}>
      <App />
    </Provider>
  );
}

export default AppWithProvider;