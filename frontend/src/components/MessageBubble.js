import React, { useState } from 'react';
import styled from 'styled-components';
import { motion } from 'framer-motion';
import ReactMarkdown from 'react-markdown';
import { Prism as SyntaxHighlighter } from 'react-syntax-highlighter';
import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';

const BubbleContainer = styled(motion.div)`
  display: flex;
  justify-content: ${props => props.isUser ? 'flex-end' : 'flex-start'};
  margin-bottom: 1rem;
`;

const Bubble = styled.div`
  max-width: 70%;
  padding: 1rem 1.25rem;
  border-radius: 1.25rem;
  position: relative;
  
  ${props => props.isUser ? `
    background: ${props.theme.colors.primary};
    color: white;
    border-bottom-right-radius: 0.25rem;
  ` : `
    background: ${props.theme.colors.surface};
    color: ${props.theme.colors.text.primary};
    border: 1px solid ${props.theme.colors.border};
    border-bottom-left-radius: 0.25rem;
  `}
`;

const MessageContent = styled.div`
  line-height: 1.5;
  word-wrap: break-word;
  
  p {
    margin: 0 0 0.5rem 0;
    
    &:last-child {
      margin-bottom: 0;
    }
  }
  
  ul, ol {
    margin: 0.5rem 0;
    padding-left: 1.5rem;
  }
  
  li {
    margin: 0.25rem 0;
  }
  
  code {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.border};
    padding: 0.125rem 0.375rem;
    border-radius: 0.25rem;
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', monospace;
    font-size: 0.875em;
  }
  
  pre {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.1)' : props.theme.colors.background};
    border: 1px solid ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.border};
    border-radius: 0.5rem;
    padding: 1rem;
    margin: 0.5rem 0;
    overflow-x: auto;
    
    code {
      background: none;
      padding: 0;
      border-radius: 0;
    }
  }
  
  blockquote {
    border-left: 3px solid ${props => props.isUser ? 'rgba(255, 255, 255, 0.5)' : props.theme.colors.primary};
    padding-left: 1rem;
    margin: 0.5rem 0;
    font-style: italic;
    opacity: 0.8;
  }
  
  table {
    width: 100%;
    border-collapse: collapse;
    margin: 0.5rem 0;
    
    th, td {
      border: 1px solid ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.border};
      padding: 0.5rem;
      text-align: left;
    }
    
    th {
      background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.1)' : props.theme.colors.hover};
      font-weight: 600;
    }
  }
`;

const MessageHeader = styled.div`
  display: flex;
  align-items: center;
  gap: 0.5rem;
  margin-bottom: 0.5rem;
  font-size: 0.75rem;
  opacity: 0.7;
`;

const Avatar = styled.div`
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.primary};
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 600;
`;

const Timestamp = styled.span`
  font-size: 0.75rem;
  opacity: 0.6;
`;

const MessageActions = styled.div`
  display: flex;
  gap: 0.5rem;
  margin-top: 0.5rem;
  opacity: 0;
  transition: opacity 0.2s ease;
  
  ${BubbleContainer}:hover & {
    opacity: 1;
  }
`;

const ActionButton = styled(motion.button)`
  padding: 0.25rem 0.5rem;
  border: none;
  background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.hover};
  color: ${props => props.isUser ? 'white' : props.theme.colors.text.primary};
  border-radius: 0.375rem;
  font-size: 0.75rem;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.3)' : props.theme.colors.primary};
    color: white;
  }
`;

const AttachmentContainer = styled.div`
  margin-top: 0.5rem;
  padding: 0.75rem;
  background: ${props => props.isUser ? 'rgba(255, 255, 255, 0.1)' : props.theme.colors.background};
  border-radius: 0.5rem;
  border: 1px solid ${props => props.isUser ? 'rgba(255, 255, 255, 0.2)' : props.theme.colors.border};
`;

const AttachmentIcon = styled.div`
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
`;

const AttachmentName = styled.div`
  font-weight: 500;
  margin-bottom: 0.25rem;
`;

const AttachmentSize = styled.div`
  font-size: 0.75rem;
  opacity: 0.7;
`;

const ErrorMessage = styled.div`
  color: ${props => props.theme.colors.error};
  font-size: 0.875rem;
  margin-top: 0.5rem;
  padding: 0.5rem;
  background: ${props => props.theme.colors.error}20;
  border-radius: 0.375rem;
  border: 1px solid ${props => props.theme.colors.error}40;
`;

const MessageBubble = ({ message, isLast = false }) => {
  const [isExpanded, setIsExpanded] = useState(false);
  const isUser = message.role === 'user';
  
  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    try {
      const date = new Date(timestamp);
      return date.toLocaleTimeString('zh-CN', { 
        hour: '2-digit', 
        minute: '2-digit' 
      });
    } catch {
      return '';
    }
  };

  const formatFileSize = (bytes) => {
    if (!bytes) return '';
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return `${(bytes / Math.pow(1024, i)).toFixed(1)} ${sizes[i]}`;
  };

  const getAttachmentIcon = (type) => {
    const iconMap = {
      image: '🖼️',
      audio: '🎵',
      video: '🎬',
      document: '📄',
      code: '💻',
      archive: '📦',
      other: '📎'
    };
    return iconMap[type] || iconMap.other;
  };

  const renderContent = () => {
    if (message.type === 'image' && message.content) {
      return (
        <img 
          src={message.content} 
          alt="消息图片" 
          style={{ 
            maxWidth: '100%', 
            borderRadius: '0.5rem',
            margin: '0.5rem 0'
          }} 
        />
      );
    }

    if (message.type === 'code' && message.content) {
      const language = message.metadata?.language || 'text';
      return (
        <SyntaxHighlighter
          language={language}
          style={oneDark}
          customStyle={{
            margin: 0,
            borderRadius: '0.5rem',
            fontSize: '0.875rem'
          }}
        >
          {message.content}
        </SyntaxHighlighter>
      );
    }

    return (
      <ReactMarkdown
        components={{
          code({ node, inline, className, children, ...props }) {
            const match = /language-(\w+)/.exec(className || '');
            return !inline && match ? (
              <SyntaxHighlighter
                language={match[1]}
                style={oneDark}
                customStyle={{
                  margin: 0,
                  borderRadius: '0.5rem',
                  fontSize: '0.875rem'
                }}
                {...props}
              >
                {String(children).replace(/\n$/, '')}
              </SyntaxHighlighter>
            ) : (
              <code className={className} {...props}>
                {children}
              </code>
            );
          }
        }}
      >
        {message.content}
      </ReactMarkdown>
    );
  };

  return (
    <BubbleContainer
      isUser={isUser}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.3 }}
    >
      <Bubble isUser={isUser}>
        <MessageHeader>
          <Avatar isUser={isUser}>
            {isUser ? 'U' : 'AI'}
          </Avatar>
          <span>{isUser ? '您' : '羲和AI'}</span>
          {message.timestamp && (
            <Timestamp>{formatTimestamp(message.timestamp)}</Timestamp>
          )}
        </MessageHeader>

        <MessageContent isUser={isUser}>
          {renderContent()}
          
          {message.attachments && message.attachments.length > 0 && (
            <AttachmentContainer isUser={isUser}>
              {message.attachments.map((attachment, index) => (
                <div key={index}>
                  <AttachmentIcon>
                    {getAttachmentIcon(attachment.type)}
                  </AttachmentIcon>
                  <AttachmentName>{attachment.name}</AttachmentName>
                  <AttachmentSize>
                    {formatFileSize(attachment.size)}
                  </AttachmentSize>
                </div>
              ))}
            </AttachmentContainer>
          )}
          
          {message.error && (
            <ErrorMessage>
              {message.error}
            </ErrorMessage>
          )}
        </MessageContent>

        <MessageActions>
          <ActionButton
            isUser={isUser}
            onClick={() => setIsExpanded(!isExpanded)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isExpanded ? '收起' : '展开'}
          </ActionButton>
          
          <ActionButton
            isUser={isUser}
            onClick={() => navigator.clipboard?.writeText(message.content)}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            复制
          </ActionButton>
        </MessageActions>
      </Bubble>
    </BubbleContainer>
  );
};

export default MessageBubble;