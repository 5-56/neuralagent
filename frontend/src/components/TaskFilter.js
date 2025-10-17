import React from 'react';
import styled from 'styled-components';

const FilterContainer = styled.div`
  display: flex;
  gap: 1rem;
  align-items: center;
  flex-wrap: wrap;
`;

const FilterGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
`;

const Label = styled.label`
  font-size: 0.875rem;
  font-weight: 500;
  color: ${props => props.theme.colors.text.secondary};
`;

const Select = styled.select`
  padding: 0.5rem 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.375rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
  font-size: 0.875rem;
  min-width: 120px;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px ${props => props.theme.colors.primary}20;
  }
`;

const SearchInput = styled.input`
  padding: 0.5rem 0.75rem;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 0.375rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
  font-size: 0.875rem;
  min-width: 200px;
  
  &:focus {
    outline: none;
    border-color: ${props => props.theme.colors.primary};
    box-shadow: 0 0 0 2px ${props => props.theme.colors.primary}20;
  }
  
  &::placeholder {
    color: ${props => props.theme.colors.text.secondary};
  }
`;

const TaskFilter = ({ 
  filter, 
  onFilterChange, 
  searchQuery, 
  onSearchChange 
}) => {
  const statusOptions = [
    { value: 'all', label: '全部状态' },
    { value: 'pending', label: '等待中' },
    { value: 'running', label: '运行中' },
    { value: 'completed', label: '已完成' },
    { value: 'failed', label: '失败' },
    { value: 'cancelled', label: '已取消' }
  ];

  const priorityOptions = [
    { value: 'all', label: '全部优先级' },
    { value: 'low', label: '低' },
    { value: 'normal', label: '普通' },
    { value: 'high', label: '高' },
    { value: 'urgent', label: '紧急' }
  ];

  const typeOptions = [
    { value: 'all', label: '全部类型' },
    { value: 'desktop_automation', label: '桌面自动化' },
    { value: 'web_automation', label: '网页自动化' },
    { value: 'file_processing', label: '文件处理' },
    { value: 'data_analysis', label: '数据分析' },
    { value: 'communication', label: '通信' },
    { value: 'custom', label: '自定义' }
  ];

  return (
    <FilterContainer>
      <FilterGroup>
        <Label>状态</Label>
        <Select
          value={filter}
          onChange={(e) => onFilterChange(e.target.value)}
        >
          {statusOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </FilterGroup>

      <FilterGroup>
        <Label>优先级</Label>
        <Select
          value={priorityOptions[0].value}
          onChange={() => {}} // 这里可以添加优先级筛选逻辑
        >
          {priorityOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </FilterGroup>

      <FilterGroup>
        <Label>类型</Label>
        <Select
          value={typeOptions[0].value}
          onChange={() => {}} // 这里可以添加类型筛选逻辑
        >
          {typeOptions.map(option => (
            <option key={option.value} value={option.value}>
              {option.label}
            </option>
          ))}
        </Select>
      </FilterGroup>

      <FilterGroup>
        <Label>搜索</Label>
        <SearchInput
          type="text"
          value={searchQuery}
          onChange={(e) => onSearchChange(e.target.value)}
          placeholder="搜索任务标题或描述..."
        />
      </FilterGroup>
    </FilterContainer>
  );
};

export default TaskFilter;