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
      tasks: [],
      currentTask: null,
      taskHistory: [],
      isTaskRunning: false,
      
      // 聊天状态
      conversations: [],
      currentConversation: null,
      messages: [],
      chatHistory: [],
      currentChat: null,
      isTyping: false,
      
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
      },
      
      // 任务管理
      fetchTasks: async () => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 1000));
          const mockTasks = [
            {
              id: 1,
              title: '示例任务1',
              description: '这是一个示例任务',
              status: 'pending',
              priority: 'normal',
              task_type: 'desktop_automation',
              progress: 0,
              created_at: new Date().toISOString()
            },
            {
              id: 2,
              title: '示例任务2',
              description: '这是另一个示例任务',
              status: 'running',
              priority: 'high',
              task_type: 'web_automation',
              progress: 50,
              created_at: new Date().toISOString()
            }
          ];
          set({ tasks: mockTasks, isLoading: false });
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      createTask: async (taskData) => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          const newTask = {
            id: Date.now(),
            ...taskData,
            status: 'pending',
            progress: 0,
            created_at: new Date().toISOString()
          };
          set(state => ({ tasks: [...state.tasks, newTask], isLoading: false }));
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      updateTask: async (taskId, taskData) => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          set(state => ({
            tasks: state.tasks.map(task => 
              task.id === taskId ? { ...task, ...taskData } : task
            ),
            isLoading: false
          }));
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      deleteTask: async (taskId) => {
        set({ isLoading: true });
        try {
          // 模拟API调用
          await new Promise(resolve => setTimeout(resolve, 500));
          set(state => ({
            tasks: state.tasks.filter(task => task.id !== taskId),
            isLoading: false
          }));
        } catch (error) {
          set({ error: error.message, isLoading: false });
        }
      },
      
      // 对话管理
      sendMessage: async (messageData) => {
        set({ isTyping: true });
        try {
          // 添加用户消息
          const userMessage = {
            id: Date.now(),
            role: 'user',
            content: messageData.content,
            timestamp: new Date().toISOString()
          };
          
          set(state => ({
            messages: [...state.messages, userMessage]
          }));
          
          // 模拟AI响应
          setTimeout(() => {
            const aiMessage = {
              id: Date.now() + 1,
              role: 'assistant',
              content: '这是一个模拟的AI响应。我理解您的需求，正在为您处理...',
              timestamp: new Date().toISOString()
            };
            
            set(state => ({
              messages: [...state.messages, aiMessage],
              isTyping: false
            }));
          }, 2000);
        } catch (error) {
          set({ error: error.message, isTyping: false });
        }
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