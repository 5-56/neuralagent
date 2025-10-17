// 羲和应用主题配置

export const lightTheme = {
  colors: {
    // 主色调
    primary: '#3b82f6',
    primaryHover: '#2563eb',
    primaryLight: '#dbeafe',
    
    // 背景色
    background: '#ffffff',
    surface: '#f8fafc',
    surfaceHover: '#f1f5f9',
    
    // 文本色
    text: {
      primary: '#1e293b',
      secondary: '#64748b',
      tertiary: '#94a3b8',
      inverse: '#ffffff'
    },
    
    // 边框和分割线
    border: '#e2e8f0',
    borderLight: '#f1f5f9',
    borderDark: '#cbd5e1',
    
    // 状态色
    success: '#10b981',
    successLight: '#d1fae5',
    warning: '#f59e0b',
    warningLight: '#fef3c7',
    error: '#ef4444',
    errorLight: '#fee2e2',
    info: '#3b82f6',
    infoLight: '#dbeafe',
    
    // 交互色
    hover: '#f1f5f9',
    active: '#e2e8f0',
    disabled: '#f8fafc',
    
    // 阴影
    shadow: {
      sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
      md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)',
      lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05)',
      xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)'
    }
  },
  
  // 字体
  fonts: {
    primary: '-apple-system, BlinkMacSystemFont, "Segoe UI", "Roboto", "Oxygen", "Ubuntu", "Cantarell", "Fira Sans", "Droid Sans", "Helvetica Neue", sans-serif',
    mono: '"Monaco", "Menlo", "Ubuntu Mono", monospace'
  },
  
  // 字体大小
  fontSizes: {
    xs: '0.75rem',
    sm: '0.875rem',
    base: '1rem',
    lg: '1.125rem',
    xl: '1.25rem',
    '2xl': '1.5rem',
    '3xl': '1.875rem',
    '4xl': '2.25rem'
  },
  
  // 字体权重
  fontWeights: {
    normal: 400,
    medium: 500,
    semibold: 600,
    bold: 700
  },
  
  // 行高
  lineHeights: {
    tight: 1.25,
    normal: 1.5,
    relaxed: 1.75
  },
  
  // 间距
  spacing: {
    xs: '0.25rem',
    sm: '0.5rem',
    md: '1rem',
    lg: '1.5rem',
    xl: '2rem',
    '2xl': '3rem',
    '3xl': '4rem'
  },
  
  // 圆角
  borderRadius: {
    none: '0',
    sm: '0.125rem',
    md: '0.375rem',
    lg: '0.5rem',
    xl: '0.75rem',
    '2xl': '1rem',
    full: '9999px'
  },
  
  // 过渡
  transitions: {
    fast: '0.15s ease-in-out',
    normal: '0.2s ease-in-out',
    slow: '0.3s ease-in-out'
  },
  
  // 断点
  breakpoints: {
    sm: '640px',
    md: '768px',
    lg: '1024px',
    xl: '1280px',
    '2xl': '1536px'
  }
};

export const darkTheme = {
  ...lightTheme,
  colors: {
    // 主色调
    primary: '#60a5fa',
    primaryHover: '#3b82f6',
    primaryLight: '#1e3a8a',
    
    // 背景色
    background: '#0f172a',
    surface: '#1e293b',
    surfaceHover: '#334155',
    
    // 文本色
    text: {
      primary: '#f8fafc',
      secondary: '#cbd5e1',
      tertiary: '#94a3b8',
      inverse: '#0f172a'
    },
    
    // 边框和分割线
    border: '#334155',
    borderLight: '#475569',
    borderDark: '#1e293b',
    
    // 状态色
    success: '#34d399',
    successLight: '#064e3b',
    warning: '#fbbf24',
    warningLight: '#451a03',
    error: '#f87171',
    errorLight: '#7f1d1d',
    info: '#60a5fa',
    infoLight: '#1e3a8a',
    
    // 交互色
    hover: '#334155',
    active: '#475569',
    disabled: '#1e293b',
    
    // 阴影
    shadow: {
      sm: '0 1px 2px 0 rgba(0, 0, 0, 0.3)',
      md: '0 4px 6px -1px rgba(0, 0, 0, 0.4), 0 2px 4px -1px rgba(0, 0, 0, 0.3)',
      lg: '0 10px 15px -3px rgba(0, 0, 0, 0.4), 0 4px 6px -2px rgba(0, 0, 0, 0.3)',
      xl: '0 20px 25px -5px rgba(0, 0, 0, 0.4), 0 10px 10px -5px rgba(0, 0, 0, 0.3)'
    }
  }
};

// CSS变量
export const cssVariables = {
  light: {
    '--color-primary': lightTheme.colors.primary,
    '--color-primary-hover': lightTheme.colors.primaryHover,
    '--color-background': lightTheme.colors.background,
    '--color-surface': lightTheme.colors.surface,
    '--color-text-primary': lightTheme.colors.text.primary,
    '--color-text-secondary': lightTheme.colors.text.secondary,
    '--color-border': lightTheme.colors.border,
    '--color-success': lightTheme.colors.success,
    '--color-warning': lightTheme.colors.warning,
    '--color-error': lightTheme.colors.error,
    '--color-info': lightTheme.colors.info
  },
  dark: {
    '--color-primary': darkTheme.colors.primary,
    '--color-primary-hover': darkTheme.colors.primaryHover,
    '--color-background': darkTheme.colors.background,
    '--color-surface': darkTheme.colors.surface,
    '--color-text-primary': darkTheme.colors.text.primary,
    '--color-text-secondary': darkTheme.colors.text.secondary,
    '--color-border': darkTheme.colors.border,
    '--color-success': darkTheme.colors.success,
    '--color-warning': darkTheme.colors.warning,
    '--color-error': darkTheme.colors.error,
    '--color-info': darkTheme.colors.info
  }
};