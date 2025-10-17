import React from 'react';
import styled, { keyframes } from 'styled-components';

const fadeIn = keyframes`
  from { opacity: 0; }
  to { opacity: 1; }
`;

const spin = keyframes`
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
`;

const pulse = keyframes`
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
`;

const Container = styled.div`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  animation: ${fadeIn} 0.5s ease-in-out;
`;

const Logo = styled.div`
  font-size: 4rem;
  font-weight: bold;
  margin-bottom: 2rem;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
`;

const Spinner = styled.div`
  width: 60px;
  height: 60px;
  border: 4px solid rgba(255, 255, 255, 0.3);
  border-top: 4px solid white;
  border-radius: 50%;
  animation: ${spin} 1s linear infinite;
  margin-bottom: 2rem;
`;

const LoadingText = styled.div`
  font-size: 1.2rem;
  font-weight: 500;
  margin-bottom: 1rem;
  animation: ${pulse} 2s ease-in-out infinite;
`;

const SubText = styled.div`
  font-size: 0.9rem;
  opacity: 0.8;
  text-align: center;
  max-width: 300px;
`;

const LoadingScreen = () => {
  return (
    <Container>
      <Logo>羲和</Logo>
      <Spinner />
      <LoadingText>正在启动应用...</LoadingText>
      <SubText>
        智能化桌面助手正在初始化，请稍候
      </SubText>
    </Container>
  );
};

export default LoadingScreen;