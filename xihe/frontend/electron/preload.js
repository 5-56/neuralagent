/**
 * 羲和桌面应用 - Electron预加载脚本
 * 提供安全的API接口给渲染进程
 */

const { contextBridge, ipcRenderer } = require('electron');

// 暴露安全的API给渲染进程
contextBridge.exposeInMainWorld('electronAPI', {
  // 应用信息
  getAppVersion: () => ipcRenderer.invoke('get-app-version'),
  
  // 存储操作
  getStoreValue: (key) => ipcRenderer.invoke('get-store-value', key),
  setStoreValue: (key, value) => ipcRenderer.invoke('set-store-value', key, value),
  deleteStoreValue: (key) => ipcRenderer.invoke('delete-store-value', key),
  
  // 对话框
  showMessageBox: (options) => ipcRenderer.invoke('show-message-box', options),
  showSaveDialog: (options) => ipcRenderer.invoke('show-save-dialog', options),
  showOpenDialog: (options) => ipcRenderer.invoke('show-open-dialog', options),
  
  // 窗口操作
  toggleOverlay: () => ipcRenderer.invoke('toggle-overlay'),
  openSettings: () => ipcRenderer.invoke('open-settings'),
  
  // 事件监听
  onLogout: (callback) => {
    ipcRenderer.on('logout', callback);
  },
  
  onCancelAllTasksTrigger: (callback) => {
    ipcRenderer.on('cancel-all-tasks-trigger', callback);
  },
  
  onAIAgentLaunch: (callback) => {
    ipcRenderer.on('ai-agent-launch', callback);
  },
  
  onAIAgentExit: (callback) => {
    ipcRenderer.on('ai-agent-exit', callback);
  },
  
  // 移除事件监听
  removeAllListeners: (channel) => {
    ipcRenderer.removeAllListeners(channel);
  }
});