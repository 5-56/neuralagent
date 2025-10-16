import React from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { zhCN } from 'date-fns/locale';

const Card = styled(motion.div)`
  background: ${props => props.theme.colors.surface};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.75rem;
  padding: 1.5rem;
  transition: all 0.2s ease;
  cursor: pointer;
  
  &:hover {
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 1rem;
`;

const Title = styled.h3`
  font-size: 1.125rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text.primary};
  margin: 0 0 0.5rem 0;
  line-height: 1.4;
`;

const Description = styled.p`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.text.secondary};
  margin: 0;
  line-height: 1.5;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
`;

const StatusBadge = styled.span`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.75rem;
  border-radius: 1rem;
  font-size: 0.75rem;
  font-weight: 500;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  
  &.pending {
    background: ${props => props.theme.colors.warning}20;
    color: ${props => props.theme.colors.warning};
  }
  
  &.running {
    background: ${props => props.theme.colors.primary}20;
    color: ${props => props.theme.colors.primary};
  }
  
  &.completed {
    background: ${props => props.theme.colors.success}20;
    color: ${props => props.theme.colors.success};
  }
  
  &.failed {
    background: ${props => props.theme.colors.error}20;
    color: ${props => props.theme.colors.error};
  }
  
  &.cancelled {
    background: ${props => props.theme.colors.text.secondary}20;
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const PriorityBadge = styled.span`
  display: inline-flex;
  align-items: center;
  padding: 0.25rem 0.5rem;
  border-radius: 0.5rem;
  font-size: 0.75rem;
  font-weight: 500;
  margin-left: 0.5rem;
  
  &.low {
    background: ${props => props.theme.colors.success}20;
    color: ${props => props.theme.colors.success};
  }
  
  &.normal {
    background: ${props => props.theme.colors.text.secondary}20;
    color: ${props => props.theme.colors.text.secondary};
  }
  
  &.high {
    background: ${props => props.theme.colors.warning}20;
    color: ${props => props.theme.colors.warning};
  }
  
  &.urgent {
    background: ${props => props.theme.colors.error}20;
    color: ${props => props.theme.colors.error};
  }
`;

const ProgressBar = styled.div`
  width: 100%;
  height: 4px;
  background: ${props => props.theme.colors.border};
  border-radius: 2px;
  overflow: hidden;
  margin: 1rem 0;
`;

const ProgressFill = styled(motion.div)`
  height: 100%;
  background: ${props => props.theme.colors.primary};
  border-radius: 2px;
`;

const Footer = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1rem;
  padding-top: 1rem;
  border-top: 1px solid ${props => props.theme.colors.border};
`;

const MetaInfo = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const MetaItem = styled.span`
  font-size: 0.75rem;
  color: ${props => props.theme.colors.text.secondary};
`;

const Actions = styled.div`
  display: flex;
  gap: 0.5rem;
`;

const ActionButton = styled(motion.button)`
  padding: 0.5rem;
  border: none;
  background: transparent;
  color: ${props => props.theme.colors.text.secondary};
  cursor: pointer;
  border-radius: 0.375rem;
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => props.theme.colors.hover};
    color: ${props => props.theme.colors.text.primary};
  }
  
  &.danger:hover {
    background: ${props => props.theme.colors.error}20;
    color: ${props => props.theme.colors.error};
  }
`;

const RunningIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.75rem;
  color: ${props => props.theme.colors.primary};
  margin-top: 0.5rem;
`;

const Dot = styled(motion.div)`
  width: 6px;
  height: 6px;
  background: ${props => props.theme.colors.primary};
  border-radius: 50%;
`;

const TaskCard = ({ task, onEdit, onDelete, isRunning = false }) => {
  const getStatusText = (status) => {
    const statusMap = {
      pending: '等待中',
      running: '运行中',
      completed: '已完成',
      failed: '失败',
      cancelled: '已取消'
    };
    return statusMap[status] || status;
  };

  const getPriorityText = (priority) => {
    const priorityMap = {
      low: '低',
      normal: '普通',
      high: '高',
      urgent: '紧急'
    };
    return priorityMap[priority] || priority;
  };

  const formatDate = (dateString) => {
    if (!dateString) return '';
    try {
      return format(new Date(dateString), 'MM-dd HH:mm', { locale: zhCN });
    } catch {
      return dateString;
    }
  };

  const getEstimatedDuration = (duration) => {
    if (!duration) return '';
    if (duration < 60) return `${duration}秒`;
    if (duration < 3600) return `${Math.round(duration / 60)}分钟`;
    return `${Math.round(duration / 3600)}小时`;
  };

  return (
    <Card
      whileHover={{ y: -2 }}
      whileTap={{ scale: 0.98 }}
      onClick={() => onEdit && onEdit(task)}
    >
      <Header>
        <div style={{ flex: 1 }}>
          <Title>{task.title}</Title>
          {task.description && (
            <Description>{task.description}</Description>
          )}
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
          <StatusBadge className={task.status}>
            {getStatusText(task.status)}
          </StatusBadge>
          {task.priority && task.priority !== 'normal' && (
            <PriorityBadge className={task.priority}>
              {getPriorityText(task.priority)}
            </PriorityBadge>
          )}
        </div>
      </Header>

      {isRunning && (
        <RunningIndicator>
          <Dot
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ 
              duration: 1, 
              repeat: Infinity, 
              delay: 0 
            }}
          />
          <Dot
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ 
              duration: 1, 
              repeat: Infinity, 
              delay: 0.2 
            }}
          />
          <Dot
            animate={{ scale: [1, 1.2, 1] }}
            transition={{ 
              duration: 1, 
              repeat: Infinity, 
              delay: 0.4 
            }}
          />
          正在执行任务...
        </RunningIndicator>
      )}

      {task.progress !== undefined && (
        <ProgressBar>
          <ProgressFill
            initial={{ width: 0 }}
            animate={{ width: `${task.progress}%` }}
            transition={{ duration: 0.5 }}
          />
        </ProgressBar>
      )}

      <Footer>
        <MetaInfo>
          <MetaItem>
            创建: {formatDate(task.created_at)}
          </MetaItem>
          {task.estimated_duration && (
            <MetaItem>
              预计: {getEstimatedDuration(task.estimated_duration)}
            </MetaItem>
          )}
          {task.execution_time && (
            <MetaItem>
              实际: {getEstimatedDuration(task.execution_time)}
            </MetaItem>
          )}
        </MetaInfo>

        <Actions onClick={(e) => e.stopPropagation()}>
          {onEdit && (
            <ActionButton
              onClick={() => onEdit(task)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              title="编辑任务"
            >
              ✏️
            </ActionButton>
          )}
          {onDelete && (
            <ActionButton
              className="danger"
              onClick={() => onDelete(task.id)}
              whileHover={{ scale: 1.1 }}
              whileTap={{ scale: 0.9 }}
              title="删除任务"
            >
              🗑️
            </ActionButton>
          )}
        </Actions>
      </Footer>
    </Card>
  );
};

export default TaskCard;