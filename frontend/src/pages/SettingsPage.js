import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import SettingsSection from '../components/SettingsSection';
import SettingsCard from '../components/SettingsCard';
import LoadingSpinner from '../components/LoadingSpinner';

const SettingsContainer = styled.div`
  display: flex;
  height: 100%;
  background: ${props => props.theme.colors.background};
`;

const Sidebar = styled.div`
  width: 250px;
  background: ${props => props.theme.colors.surface};
  border-right: 1px solid ${props => props.theme.colors.border};
  padding: 2rem 0;
`;

const SidebarItem = styled(motion.button)`
  width: 100%;
  padding: 1rem 2rem;
  border: none;
  background: ${props => props.active ? props.theme.colors.primary : 'transparent'};
  color: ${props => props.active ? 'white' : props.theme.colors.text.primary};
  text-align: left;
  cursor: pointer;
  transition: all 0.2s ease;
  border-left: 3px solid ${props => props.active ? props.theme.colors.primary : 'transparent'};
  
  &:hover {
    background: ${props => props.active ? props.theme.colors.primary : props.theme.colors.hover};
  }
`;

const SidebarItemText = styled.div`
  font-weight: 500;
  margin-bottom: 0.25rem;
`;

const SidebarItemDesc = styled.div`
  font-size: 0.875rem;
  opacity: 0.7;
`;

const Content = styled.div`
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
`;

const Header = styled.div`
  margin-bottom: 2rem;
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text.primary};
  margin: 0 0 0.5rem 0;
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  margin: 0;
  font-size: 1rem;
`;

const SettingsGrid = styled.div`
  display: grid;
  gap: 2rem;
`;

const SaveButton = styled(motion.button)`
  position: fixed;
  bottom: 2rem;
  right: 2rem;
  padding: 1rem 2rem;
  background: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 0.75rem;
  font-weight: 600;
  cursor: pointer;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
  
  &:hover {
    background: ${props => props.theme.colors.primaryHover};
  }
`;

const SettingsPage = () => {
  const {
    userSettings,
    aiSettings,
    isLoading,
    updateUserSettings,
    updateAISettings,
    saveSettings
  } = useAppStore();

  const [activeSection, setActiveSection] = useState('general');
  const [hasChanges, setHasChanges] = useState(false);
  const [localSettings, setLocalSettings] = useState({});

  const sections = [
    {
      id: 'general',
      title: '常规设置',
      description: '基本应用设置',
      icon: '⚙️'
    },
    {
      id: 'ai',
      title: 'AI设置',
      description: 'AI提供商和模型配置',
      icon: '🤖'
    },
    {
      id: 'desktop',
      title: '桌面自动化',
      description: '桌面操作相关设置',
      icon: '🖥️'
    },
    {
      id: 'voice',
      title: '语音设置',
      description: '语音识别和合成',
      icon: '🎤'
    },
    {
      id: 'notifications',
      title: '通知设置',
      description: '消息和提醒配置',
      icon: '🔔'
    },
    {
      id: 'security',
      title: '安全设置',
      description: '隐私和安全配置',
      icon: '🔒'
    },
    {
      id: 'advanced',
      title: '高级设置',
      description: '高级功能和调试',
      icon: '🔧'
    }
  ];

  useEffect(() => {
    if (userSettings && aiSettings) {
      setLocalSettings({
        ...userSettings,
        ...aiSettings
      });
    }
  }, [userSettings, aiSettings]);

  const handleSettingChange = (section, key, value) => {
    setLocalSettings(prev => ({
      ...prev,
      [key]: value
    }));
    setHasChanges(true);
  };

  const handleSave = async () => {
    try {
      await saveSettings(localSettings);
      setHasChanges(false);
    } catch (error) {
      console.error('保存设置失败:', error);
    }
  };

  const renderSectionContent = () => {
    switch (activeSection) {
      case 'general':
        return (
          <SettingsSection title="常规设置">
            <SettingsCard
              title="外观"
              description="主题和显示设置"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>主题模式</label>
                  <select
                    value={localSettings.theme || 'auto'}
                    onChange={(e) => handleSettingChange('general', 'theme', e.target.value)}
                  >
                    <option value="light">浅色</option>
                    <option value="dark">深色</option>
                    <option value="auto">自动</option>
                  </select>
                </div>
                
                <div>
                  <label>语言</label>
                  <select
                    value={localSettings.language || 'zh-CN'}
                    onChange={(e) => handleSettingChange('general', 'language', e.target.value)}
                  >
                    <option value="zh-CN">中文（简体）</option>
                    <option value="en-US">English</option>
                  </select>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'ai':
        return (
          <SettingsSection title="AI设置">
            <SettingsCard
              title="AI提供商"
              description="选择默认的AI服务提供商"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>默认提供商</label>
                  <select
                    value={localSettings.default_ai_provider || 'openai'}
                    onChange={(e) => handleSettingChange('ai', 'default_ai_provider', e.target.value)}
                  >
                    <option value="openai">OpenAI</option>
                    <option value="anthropic">Anthropic</option>
                    <option value="google">Google Gemini</option>
                    <option value="ollama">Ollama (本地)</option>
                  </select>
                </div>
                
                <div>
                  <label>默认模型</label>
                  <input
                    type="text"
                    value={localSettings.default_ai_model || ''}
                    onChange={(e) => handleSettingChange('ai', 'default_ai_model', e.target.value)}
                    placeholder="例如: gpt-4, claude-3-sonnet"
                  />
                </div>
                
                <div>
                  <label>温度 (0.0 - 1.0)</label>
                  <input
                    type="range"
                    min="0"
                    max="1"
                    step="0.1"
                    value={localSettings.ai_temperature || 0.7}
                    onChange={(e) => handleSettingChange('ai', 'ai_temperature', parseFloat(e.target.value))}
                  />
                  <span>{localSettings.ai_temperature || 0.7}</span>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'desktop':
        return (
          <SettingsSection title="桌面自动化">
            <SettingsCard
              title="自动化设置"
              description="桌面操作相关配置"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.auto_screenshot || true}
                      onChange={(e) => handleSettingChange('desktop', 'auto_screenshot', e.target.checked)}
                    />
                    自动截图
                  </label>
                </div>
                
                <div>
                  <label>截图间隔 (秒)</label>
                  <input
                    type="number"
                    min="1"
                    max="60"
                    value={localSettings.screenshot_interval || 5}
                    onChange={(e) => handleSettingChange('desktop', 'screenshot_interval', parseInt(e.target.value))}
                  />
                </div>
                
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.auto_save_logs || true}
                      onChange={(e) => handleSettingChange('desktop', 'auto_save_logs', e.target.checked)}
                    />
                    自动保存日志
                  </label>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'voice':
        return (
          <SettingsSection title="语音设置">
            <SettingsCard
              title="语音识别"
              description="语音输入相关设置"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.voice_enabled || true}
                      onChange={(e) => handleSettingChange('voice', 'voice_enabled', e.target.checked)}
                    />
                    启用语音输入
                  </label>
                </div>
                
                <div>
                  <label>语音识别语言</label>
                  <select
                    value={localSettings.voice_language || 'zh-CN'}
                    onChange={(e) => handleSettingChange('voice', 'voice_language', e.target.value)}
                  >
                    <option value="zh-CN">中文（简体）</option>
                    <option value="en-US">English</option>
                    <option value="ja-JP">日本語</option>
                  </select>
                </div>
                
                <div>
                  <label>语速</label>
                  <input
                    type="range"
                    min="0.5"
                    max="2.0"
                    step="0.1"
                    value={localSettings.voice_speed || 1.0}
                    onChange={(e) => handleSettingChange('voice', 'voice_speed', parseFloat(e.target.value))}
                  />
                  <span>{localSettings.voice_speed || 1.0}x</span>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'notifications':
        return (
          <SettingsSection title="通知设置">
            <SettingsCard
              title="消息通知"
              description="配置各种通知选项"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.email_notifications || true}
                      onChange={(e) => handleSettingChange('notifications', 'email_notifications', e.target.checked)}
                    />
                    邮件通知
                  </label>
                </div>
                
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.push_notifications || true}
                      onChange={(e) => handleSettingChange('notifications', 'push_notifications', e.target.checked)}
                    />
                    推送通知
                  </label>
                </div>
                
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.task_completion_notifications || true}
                      onChange={(e) => handleSettingChange('notifications', 'task_completion_notifications', e.target.checked)}
                    />
                    任务完成通知
                  </label>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'security':
        return (
          <SettingsSection title="安全设置">
            <SettingsCard
              title="隐私和安全"
              description="保护您的数据和隐私"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.two_factor_enabled || false}
                      onChange={(e) => handleSettingChange('security', 'two_factor_enabled', e.target.checked)}
                    />
                    启用双因素认证
                  </label>
                </div>
                
                <div>
                  <label>会话超时 (分钟)</label>
                  <input
                    type="number"
                    min="5"
                    max="1440"
                    value={localSettings.session_timeout || 60}
                    onChange={(e) => handleSettingChange('security', 'session_timeout', parseInt(e.target.value))}
                  />
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      case 'advanced':
        return (
          <SettingsSection title="高级设置">
            <SettingsCard
              title="调试和日志"
              description="高级功能和调试选项"
            >
              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                <div>
                  <label>日志级别</label>
                  <select
                    value={localSettings.log_level || 'INFO'}
                    onChange={(e) => handleSettingChange('advanced', 'log_level', e.target.value)}
                  >
                    <option value="DEBUG">调试</option>
                    <option value="INFO">信息</option>
                    <option value="WARNING">警告</option>
                    <option value="ERROR">错误</option>
                  </select>
                </div>
                
                <div>
                  <label>
                    <input
                      type="checkbox"
                      checked={localSettings.enable_metrics || false}
                      onChange={(e) => handleSettingChange('advanced', 'enable_metrics', e.target.checked)}
                    />
                    启用性能监控
                  </label>
                </div>
              </div>
            </SettingsCard>
          </SettingsSection>
        );

      default:
        return null;
    }
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <SettingsContainer>
      <Sidebar>
        {sections.map((section) => (
          <SidebarItem
            key={section.id}
            active={activeSection === section.id}
            onClick={() => setActiveSection(section.id)}
            whileHover={{ x: 5 }}
            whileTap={{ scale: 0.98 }}
          >
            <SidebarItemText>
              {section.icon} {section.title}
            </SidebarItemText>
            <SidebarItemDesc>
              {section.description}
            </SidebarItemDesc>
          </SidebarItem>
        ))}
      </Sidebar>

      <Content>
        <Header>
          <Title>设置</Title>
          <Subtitle>配置您的羲和AI助手</Subtitle>
        </Header>

        <SettingsGrid>
          {renderSectionContent()}
        </SettingsGrid>
      </Content>

      {hasChanges && (
        <SaveButton
          onClick={handleSave}
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          保存设置
        </SaveButton>
      )}
    </SettingsContainer>
  );
};

export default SettingsPage;