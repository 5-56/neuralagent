import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { useAppStore } from '../store/useAppStore';
import MessageBubble from '../components/MessageBubble';
import ChatInput from '../components/ChatInput';
import ChatHeader from '../components/ChatHeader';
import LoadingSpinner from '../components/LoadingSpinner';

const ChatContainer = styled.div`
  display: flex;
  flex-direction: column;
  height: 100%;
  background: ${props => props.theme.colors.background};
`;

const MessagesContainer = styled.div`
  flex: 1;
  overflow-y: auto;
  padding: 1rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const MessageList = styled.div`
  display: flex;
  flex-direction: column;
  gap: 1rem;
  min-height: 100%;
  justify-content: flex-end;
`;

const EmptyState = styled(motion.div)`
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
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

const TypingIndicator = styled(motion.div)`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 1rem;
  background: ${props => props.theme.colors.surface};
  border-radius: 1rem;
  margin-left: 3rem;
  max-width: 200px;
`;

const TypingDots = styled.div`
  display: flex;
  gap: 0.25rem;
`;

const Dot = styled(motion.div)`
  width: 8px;
  height: 8px;
  background: ${props => props.theme.colors.primary};
  border-radius: 50%;
`;

const TypingText = styled.span`
  font-size: 0.875rem;
  color: ${props => props.theme.colors.text.secondary};
`;

const ErrorMessage = styled(motion.div)`
  background: ${props => props.theme.colors.error};
  color: white;
  padding: 1rem;
  border-radius: 0.5rem;
  margin: 1rem;
  text-align: center;
`;

const ChatPage = () => {
  const {
    currentConversation,
    messages,
    isLoading,
    error,
    sendMessage,
    clearError,
    isTyping
  } = useAppStore();

  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef(null);
  const messagesContainerRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => {
        clearError();
      }, 5000);
      return () => clearTimeout(timer);
    }
  }, [error, clearError]);

  const handleSendMessage = async (content, type = 'text') => {
    if (!content.trim()) return;

    try {
      await sendMessage({
        content: content.trim(),
        type,
        role: 'user'
      });
      setInputValue('');
    } catch (error) {
      console.error('发送消息失败:', error);
    }
  };

  const handleVoiceInput = async (transcript) => {
    if (transcript.trim()) {
      await handleSendMessage(transcript, 'voice');
    }
  };

  const handleFileUpload = async (file) => {
    // 处理文件上传
    console.log('上传文件:', file);
  };

  if (isLoading && messages.length === 0) {
    return <LoadingSpinner />;
  }

  return (
    <ChatContainer>
      <ChatHeader conversation={currentConversation} />
      
      <MessagesContainer ref={messagesContainerRef}>
        {messages.length === 0 ? (
          <EmptyState
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
          >
            <EmptyIcon>💬</EmptyIcon>
            <EmptyTitle>开始对话</EmptyTitle>
            <EmptyDescription>
              与羲和AI助手开始对话，我可以帮助您执行各种桌面自动化任务
            </EmptyDescription>
          </EmptyState>
        ) : (
          <MessageList>
            <AnimatePresence>
              {messages.map((message, index) => (
                <motion.div
                  key={message.id || index}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                  transition={{ delay: index * 0.1 }}
                >
                  <MessageBubble
                    message={message}
                    isLast={index === messages.length - 1}
                  />
                </motion.div>
              ))}
              
              {isTyping && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, y: -20 }}
                >
                  <TypingIndicator>
                    <TypingDots>
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
                    </TypingDots>
                    <TypingText>AI正在思考...</TypingText>
                  </TypingIndicator>
                </motion.div>
              )}
            </AnimatePresence>
            <div ref={messagesEndRef} />
          </MessageList>
        )}
      </MessagesContainer>

      <AnimatePresence>
        {error && (
          <ErrorMessage
            initial={{ opacity: 0, y: 50 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 50 }}
          >
            {error}
          </ErrorMessage>
        )}
      </AnimatePresence>

      <ChatInput
        value={inputValue}
        onChange={setInputValue}
        onSend={handleSendMessage}
        onVoiceInput={handleVoiceInput}
        onFileUpload={handleFileUpload}
        disabled={isLoading}
        placeholder="输入消息或使用语音输入..."
      />
    </ChatContainer>
  );
};

export default ChatPage;