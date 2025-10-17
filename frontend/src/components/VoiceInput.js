/**
 * 语音输入组件
 */

import React, { useState, useEffect, useRef } from 'react';
import styled from 'styled-components';
import { motion, AnimatePresence } from 'framer-motion';
import { FiMic, FiMicOff, FiX } from 'react-icons/fi';

const VoiceContainer = styled(motion.div)`
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 1000;
`;

const VoiceButton = styled(motion.button)`
  width: 64px;
  height: 64px;
  border-radius: 50%;
  border: none;
  background: ${props => props.isActive 
    ? 'linear-gradient(135deg, #ef4444 0%, #dc2626 100%)' 
    : 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
  };
  color: white;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 24px;
  cursor: pointer;
  box-shadow: ${props => props.isActive 
    ? '0 8px 32px rgba(239, 68, 68, 0.4)' 
    : '0 4px 16px rgba(102, 126, 234, 0.3)'
  };
  transition: all 0.3s ease;
  
  &:hover {
    transform: scale(1.05);
  }
  
  &:active {
    transform: scale(0.95);
  }
`;

const VoicePanel = styled(motion.div)`
  position: absolute;
  bottom: 80px;
  right: 0;
  width: 320px;
  background: ${props => props.theme.colors.cardBackground};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 16px;
  padding: 24px;
  box-shadow: ${props => props.theme.shadows.modal};
`;

const StatusText = styled.div`
  text-align: center;
  font-size: 16px;
  font-weight: 600;
  color: ${props => props.theme.colors.text};
  margin-bottom: 16px;
`;

const Waveform = styled.div`
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  margin-bottom: 16px;
`;

const Bar = styled(motion.div)`
  width: 4px;
  height: 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 2px;
`;

const TranscriptText = styled.div`
  background: ${props => props.theme.colors.backgroundSecondary};
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 8px;
  padding: 12px;
  font-size: 14px;
  color: ${props => props.theme.colors.text};
  min-height: 60px;
  max-height: 120px;
  overflow-y: auto;
  margin-bottom: 16px;
`;

const ActionButtons = styled.div`
  display: flex;
  gap: 12px;
`;

const ActionButton = styled.button`
  flex: 1;
  padding: 12px;
  border: 1px solid ${props => props.theme.colors.border};
  border-radius: 8px;
  background: ${props => props.primary 
    ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
    : props.theme.colors.backgroundSecondary
  };
  color: ${props => props.primary ? 'white' : props.theme.colors.text};
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  
  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }
`;

const VoiceInput = ({ isActive, onToggle, onTranscript }) => {
  const [isListening, setIsListening] = useState(false);
  const [transcript, setTranscript] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const recognitionRef = useRef(null);
  const animationRef = useRef(null);

  // 初始化语音识别
  useEffect(() => {
    if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
      const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      
      recognitionRef.current.continuous = true;
      recognitionRef.current.interimResults = true;
      recognitionRef.current.lang = 'zh-CN';
      
      recognitionRef.current.onstart = () => {
        setIsListening(true);
        startWaveformAnimation();
      };
      
      recognitionRef.current.onresult = (event) => {
        let finalTranscript = '';
        let interimTranscript = '';
        
        for (let i = event.resultIndex; i < event.results.length; i++) {
          const transcript = event.results[i][0].transcript;
          if (event.results[i].isFinal) {
            finalTranscript += transcript;
          } else {
            interimTranscript += transcript;
          }
        }
        
        setTranscript(finalTranscript + interimTranscript);
      };
      
      recognitionRef.current.onend = () => {
        setIsListening(false);
        stopWaveformAnimation();
      };
      
      recognitionRef.current.onerror = (event) => {
        console.error('语音识别错误:', event.error);
        setIsListening(false);
        stopWaveformAnimation();
      };
    }
  }, []);

  // 开始波形动画
  const startWaveformAnimation = () => {
    const bars = document.querySelectorAll('.waveform-bar');
    bars.forEach((bar, index) => {
      bar.style.animation = `waveform ${0.5 + index * 0.1}s ease-in-out infinite alternate`;
    });
  };

  // 停止波形动画
  const stopWaveformAnimation = () => {
    const bars = document.querySelectorAll('.waveform-bar');
    bars.forEach(bar => {
      bar.style.animation = 'none';
    });
  };

  // 开始/停止语音识别
  const handleToggleListening = () => {
    if (isListening) {
      recognitionRef.current?.stop();
    } else {
      setTranscript('');
      recognitionRef.current?.start();
    }
  };

  // 发送转录结果
  const handleSendTranscript = () => {
    if (transcript.trim()) {
      setIsProcessing(true);
      onTranscript(transcript);
      setTranscript('');
      setIsProcessing(false);
      onToggle();
    }
  };

  // 取消语音输入
  const handleCancel = () => {
    recognitionRef.current?.stop();
    setTranscript('');
    onToggle();
  };

  return (
    <VoiceContainer>
      <VoiceButton
        isActive={isActive}
        onClick={onToggle}
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
      >
        {isActive ? <FiMicOff /> : <FiMic />}
      </VoiceButton>

      <AnimatePresence>
        {isActive && (
          <VoicePanel
            initial={{ opacity: 0, y: 20, scale: 0.9 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.9 }}
            transition={{ duration: 0.2 }}
          >
            <StatusText>
              {isListening ? '正在听取您的语音...' : '点击麦克风开始语音输入'}
            </StatusText>

            {isListening && (
              <Waveform>
                {[...Array(5)].map((_, i) => (
                  <Bar
                    key={i}
                    className="waveform-bar"
                    animate={{
                      height: [20, 40, 20],
                    }}
                    transition={{
                      duration: 0.5 + i * 0.1,
                      repeat: Infinity,
                      repeatType: 'reverse',
                    }}
                  />
                ))}
              </Waveform>
            )}

            <TranscriptText>
              {transcript || '语音转录结果将显示在这里...'}
            </TranscriptText>

            <ActionButtons>
              <ActionButton onClick={handleCancel}>
                <FiX style={{ marginRight: '8px' }} />
                取消
              </ActionButton>
              <ActionButton 
                primary 
                onClick={handleSendTranscript}
                disabled={!transcript.trim() || isProcessing}
              >
                {isProcessing ? '处理中...' : '发送'}
              </ActionButton>
            </ActionButtons>
          </VoicePanel>
        )}
      </AnimatePresence>

      <style jsx>{`
        @keyframes waveform {
          0% { height: 20px; }
          100% { height: 40px; }
        }
      `}</style>
    </VoiceContainer>
  );
};

export default VoiceInput;