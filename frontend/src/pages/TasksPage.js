import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import TaskCard from '../components/TaskCard';
import TaskForm from '../components/TaskForm';
import TaskFilter from '../components/TaskFilter';
import LoadingSpinner from '../components/LoadingSpinner';

const TasksContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: ${props => props.theme.colors.background};
`;

const Header = styled.div`
  padding: 2rem;
  border-bottom: 1px solid ${props => props.theme.colors.border};
  background: ${props => props.theme.colors.surface};
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text.primary};
  margin: 0 0 1rem 0;
`;

const Subtitle = styled.p`
  color: ${props => props.theme.colors.text.secondary};
  margin: 0;
  font-size: 1rem;
`;

const Controls = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 1.5rem;
  gap: 1rem;
`;

const Button = styled(motion.button)`
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 0.5rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &.primary {
    background: ${props => props.theme.colors.primary};
    color: white;
    
    &:hover {
      background: ${props => props.theme.colors.primaryHover};
    }
  }
  
  &.secondary {
    background: ${props => props.theme.colors.surface};
    color: ${props => props.theme.colors.text.primary};
    border: 1px solid ${props => props.theme.colors.border};
    
    &:hover {
      background: ${props => props.theme.colors.hover};
    }
  }
`;

const Content = styled.div`
  flex: 1;
  padding: 2rem;
  overflow-y: auto;
`;

const TasksGrid = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
`;

const EmptyState = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 4rem 2rem;
  text-align: center;
  color: ${props => props.theme.colors.text.secondary};
`;

const EmptyIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  opacity: 0.5;
`;

const EmptyTitle = styled.h3`
  font-size: 1.5rem;
  font-weight: 600;
  margin: 0 0 0.5rem 0;
  color: ${props => props.theme.colors.text.primary};
`;

const EmptyDescription = styled.p`
  font-size: 1rem;
  margin: 0 0 2rem 0;
  max-width: 400px;
`;

const StatsContainer = styled.div`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1rem;
  margin-bottom: 2rem;
`;

const StatCard = styled(motion.div)`
  background: ${props => props.theme.colors.surface};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.75rem;
  padding: 1.5rem;
  text-align: center;
`;

const StatValue = styled.div`
  font-size: 2rem;
  font-weight: 700;
  color: ${props => props.theme.colors.primary};
  margin-bottom: 0.5rem;
`;

const StatLabel = styled.div`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.text.secondary};
  text-transform: uppercase;
  letter-spacing: 0.05em;
`;

const TasksPage = () => {
  const {
    tasks,
    isLoading,
    error,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    currentTask
  } = useAppStore();

  const [showTaskForm, setShowTaskForm] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [filter, setFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleCreateTask = async (taskData) => {
    try {
      await createTask(taskData);
      setShowTaskForm(false);
    } catch (error) {
      console.error('创建任务失败:', error);
    }
  };

  const handleUpdateTask = async (taskId, taskData) => {
    try {
      await updateTask(taskId, taskData);
      setEditingTask(null);
    } catch (error) {
      console.error('更新任务失败:', error);
    }
  };

  const handleDeleteTask = async (taskId) => {
    if (window.confirm('确定要删除这个任务吗？')) {
      try {
        await deleteTask(taskId);
      } catch (error) {
        console.error('删除任务失败:', error);
      }
    }
  };

  const filteredTasks = tasks.filter(task => {
    const matchesFilter = filter === 'all' || task.status === filter;
    const matchesSearch = task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                         task.description?.toLowerCase().includes(searchQuery.toLowerCase());
    return matchesFilter && matchesSearch;
  });

  const stats = {
    total: tasks.length,
    running: tasks.filter(t => t.status === 'running').length,
    completed: tasks.filter(t => t.status === 'completed').length,
    failed: tasks.filter(t => t.status === 'failed').length
  };

  if (isLoading) {
    return <LoadingSpinner />;
  }

  return (
    <TasksContainer>
      <Header>
        <Title>任务管理</Title>
        <Subtitle>管理和监控您的自动化任务</Subtitle>
        
        <Controls>
          <TaskFilter
            filter={filter}
            onFilterChange={setFilter}
            searchQuery={searchQuery}
            onSearchChange={setSearchQuery}
          />
          
          <div style={{ display: 'flex', gap: '1rem' }}>
            <Button
              className="secondary"
              onClick={() => setShowTaskForm(true)}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
            >
              创建任务
            </Button>
          </div>
        </Controls>
      </Header>

      <Content>
        <StatsContainer>
          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <StatValue>{stats.total}</StatValue>
            <StatLabel>总任务</StatLabel>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <StatValue>{stats.running}</StatValue>
            <StatLabel>运行中</StatLabel>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <StatValue>{stats.completed}</StatValue>
            <StatLabel>已完成</StatLabel>
          </StatCard>
          
          <StatCard
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <StatValue>{stats.failed}</StatValue>
            <StatLabel>失败</StatLabel>
          </StatCard>
        </StatsContainer>

        {filteredTasks.length === 0 ? (
          <EmptyState
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <EmptyIcon>📋</EmptyIcon>
            <EmptyTitle>暂无任务</EmptyTitle>
            <EmptyDescription>
              {searchQuery ? '没有找到匹配的任务' : '开始创建您的第一个自动化任务'}
            </EmptyDescription>
            {!searchQuery && (
              <Button
                className="primary"
                onClick={() => setShowTaskForm(true)}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                创建任务
              </Button>
            )}
          </EmptyState>
        ) : (
          <TasksGrid>
            <AnimatePresence>
              {filteredTasks.map((task, index) => (
                <motion.div
                  key={task.id}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <TaskCard
                    task={task}
                    onEdit={setEditingTask}
                    onDelete={handleDeleteTask}
                    isRunning={currentTask?.id === task.id}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
          </TasksGrid>
        )}
      </Content>

      <AnimatePresence>
        {showTaskForm && (
          <TaskForm
            task={editingTask}
            onSubmit={editingTask ? 
              (data) => handleUpdateTask(editingTask.id, data) : 
              handleCreateTask
            }
            onClose={() => {
              setShowTaskForm(false);
              setEditingTask(null);
            }}
          />
        )}
      </AnimatePresence>
    </TasksContainer>
  );
};

export default TasksPage;