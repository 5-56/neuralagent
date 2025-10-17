/**
 * 羲和应用首页
 */

import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';

// 组件
import WelcomeCard from '../components/WelcomeCard';
import QuickActions from '../components/QuickActions';
import RecentTasks from '../components/RecentTasks';
import AIStatus from '../components/AIStatus';
import VoiceInput from '../components/VoiceInput';

// 样式
const HomeContainer = styled.div`
  display: flex;
  flex-direction: column;
  gap: 24px;
  height: 100%;
`;

const TopSection = styled.div`
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const BottomSection = styled.div`
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 24px;
  
  @media (max-width: 1200px) {
    grid-template-columns: 1fr;
  }
`;

const Card = styled(motion.div)`
  background: ${props => props.theme.colors.cardBackground};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 12px;
  padding: 24px;
  box-shadow: ${props => props.theme.shadows.card};
`;

const HomePage = () => {
  const { 
    isDarkMode, 
    currentTask, 
    isTaskRunning,
    startTask,
    addChatMessage 
  } = useAppStore();

  const [isVoiceActive, setIsVoiceActive] = useState(false);

  // 处理语音输入
  const handleVoiceInput = (transcript) => {
    if (transcript.trim()) {
      // 创建任务
      const task = {
        id: Date.now(),
        type: 'voice_command',
        description: transcript,
        status: 'pending',
        createdAt: new Date()
      };
      
      startTask(task);
      addChatMessage({
        type: 'user',
        content: transcript,
        source: 'voice'
      });
    }
  };

  // 处理快速操作
  const handleQuickAction = (action) => {
    const task = {
      id: Date.now(),
      type: 'quick_action',
      description: action.description,
      action: action.action,
      status: 'pending',
      createdAt: new Date()
    };
    
    startTask(task);
  };

  return (
    <HomeContainer>
      {/* 顶部区域 */}
      <TopSection>
        {/* 欢迎卡片 */}
        <Card
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
        >
          <WelcomeCard 
            isTaskRunning={isTaskRunning}
            currentTask={currentTask}
          />
        </Card>

        {/* AI状态 */}
        <Card
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.1 }}
        >
          <AIStatus />
        </Card>
      </TopSection>

      {/* 底部区域 */}
      <BottomSection>
        {/* 快速操作 */}
        <Card
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.2 }}
        >
          <QuickActions onAction={handleQuickAction} />
        </Card>

        {/* 最近任务 */}
        <Card
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5, delay: 0.3 }}
        >
          <RecentTasks />
        </Card>
      </BottomSection>

      {/* 语音输入 */}
      <VoiceInput
        isActive={isVoiceActive}
        onToggle={() => setIsVoiceActive(!isVoiceActive)}
        onTranscript={handleVoiceInput}
      />
    </HomeContainer>
  );
};

export default HomePage;