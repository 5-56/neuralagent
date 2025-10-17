/**
 * 欢迎卡片组件
 */

import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { FiZap, FiPlay, FiPause, FiCheckCircle } from 'react-icons/fi';

const Card = styled.div`
  display: flex;
  flex-direction: column;
  gap: 20px;
`;

const Header = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
`;

const Icon = styled.div`
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 24px;
`;

const Title = styled.h1`
  font-size: 28px;
  font-weight: 700;
  color: ${props => props.theme.colors.text};
  margin: 0;
`;

const Subtitle = styled.p`
  font-size: 16px;
  color: ${props => props.theme.colors.textSecondary};
  margin: 0;
`;

const TaskStatus = styled.div`
  padding: 16px;
  border-radius: 8px;
  background: ${props => props.theme.colors.backgroundSecondary};
  border: 1px solid ${props => props.theme.colors.border};
`;

const TaskInfo = styled.div`
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
`;

const TaskIcon = styled.div`
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: ${props => props.running ? '#10b981' : '#f59e0b'};
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
  font-size: 16px;
`;

const TaskText = styled.div`
  flex: 1;
`;

const TaskTitle = styled.div`
  font-weight: 600;
  color: ${props => props.theme.colors.text};
  margin-bottom: 4px;
`;

const TaskDescription = styled.div`
  font-size: 14px;
  color: ${props => props.theme.colors.textSecondary};
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 4px;
  background: ${props => props.theme.colors.border};
  border-radius: 2px;
  overflow: hidden;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
`;

const WelcomeCard = ({ isTaskRunning, currentTask }) => {
  return (
    <Card>
      <Header>
        <Icon>
          <FiZap />
        </Icon>
        <div>
          <Title>欢迎使用羲和</Title>
          <Subtitle>您的智能化桌面助手</Subtitle>
        </div>
      </Header>

      {isTaskRunning && currentTask ? (
        <TaskStatus>
          <TaskInfo>
            <TaskIcon running={isTaskRunning}>
              {isTaskRunning ? <FiPlay /> : <FiPause />}
            </TaskIcon>
            <TaskText>
              <TaskTitle>
                {isTaskRunning ? '正在执行任务' : '任务已暂停'}
              </TaskTitle>
              <TaskDescription>
                {currentTask.description}
              </TaskDescription>
            </TaskText>
          </TaskInfo>
          
          <ProgressBar>
            <ProgressFill
              initial={{ width: 0 }}
              animate={{ width: isTaskRunning ? '60%' : '30%' }}
              transition={{ duration: 0.5 }}
            />
          </ProgressBar>
        </TaskStatus>
      ) : (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 0.5 }}
        >
          <p style={{ 
            color: '#6b7280', 
            fontSize: '16px',
            lineHeight: '1.6',
            margin: 0
          }}>
            告诉我您想要完成的任务，我将为您自动执行。支持语音输入、文本描述或直接操作。
          </p>
        </motion.div>
      )}
    </Card>
  );
};

export default WelcomeCard;