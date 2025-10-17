import React, { useState, useEffect } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useForm } from 'react-hook-form';

const Overlay = styled(motion.div)`
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
`;

const Modal = styled(motion.div)`
  background: ${props => props.theme.colors.surface};
  border-radius: 1rem;
  padding: 2rem;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
`;

const Header = styled.div`
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
`;

const Title = styled.h2`
  font-size: 1.5rem;
  font-weight: 600;
  color: ${props => props.theme.colors.text.primary};
  margin: 0;
`;

const CloseButton = styled.button`
  background: none;
  border: none;
  font-size: 1.5rem;
  color: ${props => props.theme.colors.text.secondary};
  cursor: pointer;
  padding: 0.5rem;
  border-radius: 0.5rem;
  
  &:hover {
    background: ${props => props.theme.colors.hover};
  }
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
`;

const FormGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  font-weight: 500;
  color: ${props => props.theme.colors.text.primary};
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
  
  &.error {
    border-color: ${props => props.theme.colors.error};
  }
`;

const TextArea = styled.textarea`
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
  font-size: 1rem;
  min-height: 100px;
  resize: vertical;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
  
  &.error {
    border-color: ${props => props.theme.colors.error};
  }
`;

const Select = styled.select`
  padding: 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.5rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
  font-size: 1rem;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 3px ${props => props.theme.colors.primary}20;
  }
`;

const ButtonGroup = styled.div`
  display: flex;
  gap: 1rem;
  justify-content: flex-end;
  margin-top: 2rem;
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
    
    &:disabled {
      background: ${props => props.theme.colors.text.secondary};
      cursor: not-allowed;
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

const ErrorMessage = styled.span`
  color: ${props => props.theme.colors.error};
  font-size: 0.875rem;
  margin-top: 0.25rem;
`;

const TaskForm = ({ task, onSubmit, onClose }) => {
  const { register, handleSubmit, formState: { errors }, reset } = useForm({
    defaultValues: {
      title: task?.title || '',
      description: task?.description || '',
      task_type: task?.task_type || 'desktop_automation',
      priority: task?.priority || 'normal',
      estimated_duration: task?.estimated_duration || ''
    }
  });

  const [isSubmitting, setIsSubmitting] = useState(false);

  useEffect(() => {
    if (task) {
      reset({
        title: task.title,
        description: task.description,
        task_type: task.task_type,
        priority: task.priority,
        estimated_duration: task.estimated_duration
      });
    }
  }, [task, reset]);

  const handleFormSubmit = async (data) => {
    setIsSubmitting(true);
    try {
      await onSubmit(data);
    } catch (error) {
      console.error('提交失败:', error);
    } finally {
      setIsSubmitting(false);
    }
  };

  const taskTypes = [
    { value: 'desktop_automation', label: '桌面自动化' },
    { value: 'web_automation', label: '网页自动化' },
    { value: 'file_processing', label: '文件处理' },
    { value: 'data_analysis', label: '数据分析' },
    { value: 'communication', label: '通信' },
    { value: 'custom', label: '自定义' }
  ];

  const priorities = [
    { value: 'low', label: '低' },
    { value: 'normal', label: '普通' },
    { value: 'high', label: '高' },
    { value: 'urgent', label: '紧急' }
  ];

  return (
    <AnimatePresence>
      <Overlay
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={onClose}
      >
        <Modal
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          exit={{ scale: 0.9, opacity: 0 }}
          onClick={(e) => e.stopPropagation()}
        >
          <Header>
            <Title>{task ? '编辑任务' : '创建任务'}</Title>
            <CloseButton onClick={onClose}>×</CloseButton>
          </Header>

          <Form onSubmit={handleSubmit(handleFormSubmit)}>
            <FormGroup>
              <Label htmlFor="title">任务标题 *</Label>
              <Input
                id="title"
                type="text"
                {...register('title', { required: '请输入任务标题' })}
                className={errors.title ? 'error' : ''}
                placeholder="输入任务标题"
              />
              {errors.title && (
                <ErrorMessage>{errors.title.message}</ErrorMessage>
              )}
            </FormGroup>

            <FormGroup>
              <Label htmlFor="description">任务描述</Label>
              <TextArea
                id="description"
                {...register('description')}
                placeholder="描述任务的具体内容和目标"
              />
            </FormGroup>

            <FormGroup>
              <Label htmlFor="task_type">任务类型</Label>
              <Select id="task_type" {...register('task_type')}>
                {taskTypes.map(type => (
                  <option key={type.value} value={type.value}>
                    {type.label}
                  </option>
                ))}
              </Select>
            </FormGroup>

            <FormGroup>
              <Label htmlFor="priority">优先级</Label>
              <Select id="priority" {...register('priority')}>
                {priorities.map(priority => (
                  <option key={priority.value} value={priority.value}>
                    {priority.label}
                  </option>
                ))}
              </Select>
            </FormGroup>

            <FormGroup>
              <Label htmlFor="estimated_duration">预估执行时间（秒）</Label>
              <Input
                id="estimated_duration"
                type="number"
                min="1"
                {...register('estimated_duration', { 
                  valueAsNumber: true,
                  min: { value: 1, message: '执行时间必须大于0' }
                })}
                className={errors.estimated_duration ? 'error' : ''}
                placeholder="例如: 300"
              />
              {errors.estimated_duration && (
                <ErrorMessage>{errors.estimated_duration.message}</ErrorMessage>
              )}
            </FormGroup>

            <ButtonGroup>
              <Button
                type="button"
                className="secondary"
                onClick={onClose}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                取消
              </Button>
              <Button
                type="submit"
                className="primary"
                disabled={isSubmitting}
                whileHover={{ scale: 1.02 }}
                whileTap={{ scale: 0.98 }}
              >
                {isSubmitting ? '保存中...' : (task ? '更新' : '创建')}
              </Button>
            </ButtonGroup>
          </Form>
        </Modal>
      </Overlay>
    </AnimatePresence>
  );
};

export default TaskForm;