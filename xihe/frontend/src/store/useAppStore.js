/**
 * 羲和应用状态管理 - Zustand Store
 */

import { create } from 'zustand';
import { persist } from 'zustand/middleware';

const useAppStore = create(
  persist(
    (set, get) => ({
      // 应用状态
      isInitialized: false,
      isLoading: false,
      error: null,
      
      // 主题设置
      isDarkMode: false,
      
      // 用户信息
      user: null,
      isAuthenticated: false,
      
      // AI设置
      selectedProvider: 'openai',
      selectedModel: 'gpt-4',
      temperature: 0.7,
      maxTokens: 2000,
      
      // 任务状态
      currentTask: null,
      taskHistory: [],
      isTaskRunning: false,
      
      // 聊天状态
      chatHistory: [],
      currentChat: null,
      
      // 设置
      settings: {
        autoStart: false,
        minimizeToTray: true,
        enableOverlay: true,
        enableVoice: true,
        enableNotifications: true,
        language: 'zh-CN',
        fontSize: 'medium',
        theme: 'auto'
      },
      
      // 动作
      initializeApp: async () => {
        set({ isLoading: true });
        
        try {
          // 从Electron存储加载设置
          const storedSettings = await window.electronAPI?.getStoreValue('settings');
          const storedTheme = await window.electronAPI?.getStoreValue('theme');
          const storedUser = await window.electronAPI?.getStoreValue('user');
          
          if (storedSettings) {
            set({ settings: { ...get().settings, ...storedSettings } });
          }
          
          if (storedTheme) {
            set({ isDarkMode: storedTheme === 'dark' });
          }
          
          if (storedUser) {
            set({ user: storedUser, isAuthenticated: true });
          }
          
          set({ isInitialized: true, isLoading: false });
        } catch (error) {
          console.error('应用初始化失败:', error);
          set({ error: error.message, isLoading: false });
        }
      },
      
      setTheme: (theme) => {
        const isDark = theme === 'dark' || (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches);
        set({ isDarkMode: isDark });
        
        // 保存到Electron存储
        window.electronAPI?.setStoreValue('theme', theme);
      },
      
      setUser: (user) => {
        set({ user, isAuthenticated: !!user });
        window.electronAPI?.setStoreValue('user', user);
      },
      
      logout: () => {
        set({ 
          user: null, 
          isAuthenticated: false, 
          currentTask: null, 
          chatHistory: [] 
        });
        window.electronAPI?.deleteStoreValue('user');
      },
      
      updateSettings: (newSettings) => {
        const updatedSettings = { ...get().settings, ...newSettings };
        set({ settings: updatedSettings });
        window.electronAPI?.setStoreValue('settings', updatedSettings);
      },
      
      setAISettings: (provider, model, temperature, maxTokens) => {
        set({ 
          selectedProvider: provider,
          selectedModel: model,
          temperature,
          maxTokens
        });
      },
      
      startTask: (task) => {
        set({ 
          currentTask: task, 
          isTaskRunning: true 
        });
      },
      
      stopTask: () => {
        set({ 
          currentTask: null, 
          isTaskRunning: false 
        });
      },
      
      addChatMessage: (message) => {
        const newMessage = {
          id: Date.now(),
          timestamp: new Date(),
          ...message
        };
        
        set(state => ({
          chatHistory: [...state.chatHistory, newMessage]
        }));
      },
      
      clearChatHistory: () => {
        set({ chatHistory: [] });
      },
      
      setError: (error) => {
        set({ error });
      },
      
      clearError: () => {
        set({ error: null });
      }
    }),
    {
      name: 'xihe-app-store',
      partialize: (state) => ({
        isDarkMode: state.isDarkMode,
        settings: state.settings,
        selectedProvider: state.selectedProvider,
        selectedModel: state.selectedModel,
        temperature: state.temperature,
        maxTokens: state.maxTokens
      })
    }
  )
);

export { useAppStore };