/**
 * 羲和桌面应用 - Electron主进程
 * 负责窗口管理、系统集成和与后端的通信
 */

const { app, BrowserWindow, Menu, ipcMain, dialog, screen, shell } = require('electron');
const path = require('path');
const isDev = require('electron-is-dev');
const Store = require('electron-store');
const { spawn } = require('child_process');

// 配置存储
const store = new Store();

// 全局变量
let mainWindow;
let overlayWindow;
let settingsWindow;
let backendProcess;
let isBackendRunning = false;

// 应用配置
const APP_CONFIG = {
  name: '羲和',
  version: '1.0.0',
  minWidth: 1200,
  minHeight: 800,
  overlaySize: 60,
  overlayMargin: 25
};

/**
 * 创建主窗口
 */
function createMainWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;
  
  mainWindow = new BrowserWindow({
    width: Math.max(APP_CONFIG.minWidth, width * 0.8),
    height: Math.max(APP_CONFIG.minHeight, height * 0.8),
    minWidth: APP_CONFIG.minWidth,
    minHeight: APP_CONFIG.minHeight,
    icon: getIconPath(),
    title: APP_CONFIG.name,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      enableRemoteModule: false,
      preload: path.join(__dirname, 'preload.js')
    },
    show: false, // 先不显示，等加载完成后再显示
    titleBarStyle: process.platform === 'darwin' ? 'hiddenInset' : 'default'
  });

  // 加载应用
  const startUrl = isDev 
    ? 'http://localhost:3000' 
    : `file://${path.join(__dirname, '../build/index.html')}`;
  
  mainWindow.loadURL(startUrl);

  // 窗口准备就绪后显示
  mainWindow.once('ready-to-show', () => {
    mainWindow.show();
    
    // 开发模式下打开开发者工具
    if (isDev) {
      mainWindow.webContents.openDevTools();
    }
  });

  // 窗口关闭事件
  mainWindow.on('closed', () => {
    mainWindow = null;
  });

  // 处理外部链接
  mainWindow.webContents.setWindowOpenHandler(({ url }) => {
    shell.openExternal(url);
    return { action: 'deny' };
  });
}

/**
 * 创建悬浮窗
 */
function createOverlayWindow() {
  if (overlayWindow) return;

  const { width: screenWidth, height: screenHeight } = screen.getPrimaryDisplay().workArea;
  const windowSize = APP_CONFIG.overlaySize;
  const margin = APP_CONFIG.overlayMargin;
  
  const x = screenWidth - windowSize - margin;
  const y = screenHeight - windowSize - margin;

  overlayWindow = new BrowserWindow({
    width: windowSize,
    height: windowSize,
    x: x,
    y: y,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: false,
    skipTaskbar: true,
    icon: getIconPath(),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  const overlayUrl = isDev
    ? 'http://localhost:3000/#/overlay'
    : `file://${path.join(__dirname, '../build/index.html')}#/overlay`;

  overlayWindow.loadURL(overlayUrl);

  overlayWindow.on('closed', () => {
    overlayWindow = null;
  });
}

/**
 * 创建设置窗口
 */
function createSettingsWindow() {
  if (settingsWindow) {
    settingsWindow.focus();
    return;
  }

  settingsWindow = new BrowserWindow({
    width: 800,
    height: 600,
    parent: mainWindow,
    modal: true,
    icon: getIconPath(),
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: path.join(__dirname, 'preload.js')
    }
  });

  const settingsUrl = isDev
    ? 'http://localhost:3000/#/settings'
    : `file://${path.join(__dirname, '../build/index.html')}#/settings`;

  settingsWindow.loadURL(settingsUrl);

  settingsWindow.on('closed', () => {
    settingsWindow = null;
  });
}

/**
 * 获取图标路径
 */
function getIconPath() {
  const iconName = process.platform === 'win32' ? 'icon.ico' : 
                   process.platform === 'darwin' ? 'icon.icns' : 'icon.png';
  return path.join(__dirname, '../assets', iconName);
}

/**
 * 启动后端服务
 */
function startBackendService() {
  if (isBackendRunning) return;

  const backendPath = path.join(__dirname, '../../backend');
  const pythonCommand = process.platform === 'win32' ? 'python' : 'python3';
  
  backendProcess = spawn(pythonCommand, ['main.py'], {
    cwd: backendPath,
    env: { ...process.env, PYTHONPATH: backendPath }
  });

  backendProcess.stdout.on('data', (data) => {
    console.log(`[后端] ${data}`);
  });

  backendProcess.stderr.on('data', (data) => {
    console.error(`[后端错误] ${data}`);
  });

  backendProcess.on('close', (code) => {
    console.log(`[后端] 进程退出，代码: ${code}`);
    isBackendRunning = false;
  });

  isBackendRunning = true;
  console.log('[后端] 服务已启动');
}

/**
 * 停止后端服务
 */
function stopBackendService() {
  if (backendProcess && !backendProcess.killed) {
    backendProcess.kill();
    isBackendRunning = false;
    console.log('[后端] 服务已停止');
  }
}

/**
 * 创建应用菜单
 */
function createAppMenu() {
  const template = [
    {
      label: '羲和',
      submenu: [
        {
          label: '关于羲和',
          click: () => {
            dialog.showMessageBox(mainWindow, {
              type: 'info',
              title: '关于羲和',
              message: `${APP_CONFIG.name} v${APP_CONFIG.version}`,
              detail: '智能化桌面助手 - 让AI真正理解你的桌面世界'
            });
          }
        },
        { type: 'separator' },
        {
          label: '设置',
          accelerator: 'CmdOrCtrl+,',
          click: () => createSettingsWindow()
        },
        { type: 'separator' },
        {
          label: '退出',
          accelerator: process.platform === 'darwin' ? 'Cmd+Q' : 'Ctrl+Q',
          click: () => app.quit()
        }
      ]
    },
    {
      label: '编辑',
      submenu: [
        { role: 'undo' },
        { role: 'redo' },
        { type: 'separator' },
        { role: 'cut' },
        { role: 'copy' },
        { role: 'paste' },
        { role: 'selectall' }
      ]
    },
    {
      label: '视图',
      submenu: [
        { role: 'reload' },
        { role: 'forceReload' },
        { role: 'toggleDevTools' },
        { type: 'separator' },
        { role: 'resetZoom' },
        { role: 'zoomIn' },
        { role: 'zoomOut' },
        { type: 'separator' },
        { role: 'togglefullscreen' }
      ]
    },
    {
      label: '窗口',
      submenu: [
        { role: 'minimize' },
        { role: 'close' },
        { type: 'separator' },
        {
          label: '显示悬浮窗',
          click: () => {
            if (overlayWindow) {
              overlayWindow.close();
            } else {
              createOverlayWindow();
            }
          }
        }
      ]
    },
    {
      label: '帮助',
      submenu: [
        {
          label: '使用指南',
          click: () => {
            shell.openExternal('https://github.com/your-org/xihe/docs');
          }
        },
        {
          label: '反馈问题',
          click: () => {
            shell.openExternal('https://github.com/your-org/xihe/issues');
          }
        }
      ]
    }
  ];

  const menu = Menu.buildFromTemplate(template);
  Menu.setApplicationMenu(menu);
}

// IPC 事件处理
ipcMain.handle('get-app-version', () => APP_CONFIG.version);
ipcMain.handle('get-store-value', (event, key) => store.get(key));
ipcMain.handle('set-store-value', (event, key, value) => store.set(key, value));
ipcMain.handle('delete-store-value', (event, key) => store.delete(key));

ipcMain.handle('show-message-box', async (event, options) => {
  const result = await dialog.showMessageBox(mainWindow, options);
  return result;
});

ipcMain.handle('show-save-dialog', async (event, options) => {
  const result = await dialog.showSaveDialog(mainWindow, options);
  return result;
});

ipcMain.handle('show-open-dialog', async (event, options) => {
  const result = await dialog.showOpenDialog(mainWindow, options);
  return result;
});

ipcMain.handle('toggle-overlay', () => {
  if (overlayWindow) {
    overlayWindow.close();
  } else {
    createOverlayWindow();
  }
});

ipcMain.handle('open-settings', () => {
  createSettingsWindow();
});

// 应用事件
app.whenReady().then(() => {
  createMainWindow();
  createAppMenu();
  startBackendService();
  
  // macOS 特殊处理
  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createMainWindow();
    }
  });
});

app.on('window-all-closed', () => {
  // macOS 特殊处理
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('before-quit', () => {
  stopBackendService();
});

// 安全设置
app.on('web-contents-created', (event, contents) => {
  contents.on('new-window', (event, navigationUrl) => {
    event.preventDefault();
    shell.openExternal(navigationUrl);
  });
});

// 防止导航到外部URL
app.on('web-contents-created', (event, contents) => {
  contents.on('will-navigate', (event, navigationUrl) => {
    const parsedUrl = new URL(navigationUrl);
    
    if (parsedUrl.origin !== 'http://localhost:3000' && !navigationUrl.startsWith('file://')) {
      event.preventDefault();
    }
  });
});