import React from 'react';
import styled from 'styled-components';

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  padding: 2rem;
  background: ${props => props.theme.colors.background};
  color: ${props => props.theme.colors.text.primary};
`;

const ErrorIcon = styled.div`
  font-size: 4rem;
  margin-bottom: 1rem;
  color: ${props => props.theme.colors.error};
`;

const Title = styled.h1`
  font-size: 2rem;
  font-weight: 600;
  margin-bottom: 1rem;
  text-align: center;
`;

const Message = styled.p`
  font-size: 1rem;
  color: ${props => props.theme.colors.text.secondary};
  text-align: center;
  margin-bottom: 2rem;
  max-width: 500px;
`;

const Button = styled.button`
  padding: 0.75rem 1.5rem;
  background: ${props => props.theme.colors.primary};
  color: white;
  border: none;
  border-radius: 0.5rem;
  font-size: 1rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => props.theme.colors.primaryHover};
    transform: translateY(-2px);
  }
`;

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    this.setState({
      error: error,
      errorInfo: errorInfo
    });
    
    // 记录错误到控制台
    console.error('ErrorBoundary caught an error:', error, errorInfo);
  }

  handleReload = () => {
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <Container>
          <ErrorIcon>⚠️</ErrorIcon>
          <Title>应用出现错误</Title>
          <Message>
            很抱歉，应用遇到了一个意外错误。这可能是由于配置问题或网络连接问题导致的。
            请尝试重新加载应用，如果问题持续存在，请联系技术支持。
          </Message>
          <Button onClick={this.handleReload}>
            重新加载应用
          </Button>
        </Container>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;