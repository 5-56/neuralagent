# 语音处理工具
import os
import time
import wave
import tempfile
from typing import Optional, Dict, Any, List
import speech_recognition as sr
import pyttsx3
import pyaudio
import numpy as np
from core.config import settings

class VoiceTool:
    """语音处理工具类"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.tts_engine = pyttsx3.init()
        
        # 配置语音识别
        self.recognizer.energy_threshold = 300
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        # 配置语音合成
        self._configure_tts()
        
        # 语音文件目录
        self.voice_dir = "voice_files"
        self._ensure_voice_dir()
    
    def _ensure_voice_dir(self):
        """确保语音文件目录存在"""
        if not os.path.exists(self.voice_dir):
            os.makedirs(self.voice_dir)
    
    def _configure_tts(self):
        """配置语音合成"""
        try:
            # 设置语音属性
            voices = self.tts_engine.getProperty('voices')
            
            # 根据语言选择语音
            language = settings.SPEECH_SYNTHESIS_LANGUAGE
            if language.startswith('zh'):
                # 中文语音
                for voice in voices:
                    if 'chinese' in voice.name.lower() or 'mandarin' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            else:
                # 英文语音
                for voice in voices:
                    if 'english' in voice.name.lower():
                        self.tts_engine.setProperty('voice', voice.id)
                        break
            
            # 设置语速和音量
            self.tts_engine.setProperty('rate', 150)  # 语速
            self.tts_engine.setProperty('volume', 0.8)  # 音量
            
        except Exception as e:
            print(f"TTS配置失败: {e}")
    
    def record_audio(self, duration: int = 5, language: str = None) -> Dict[str, Any]:
        """录制音频"""
        try:
            if language is None:
                language = settings.SPEECH_RECOGNITION_LANGUAGE
            
            # 调整环境噪音
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # 录制音频
            print(f"开始录制 {duration} 秒...")
            audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # 保存音频文件
            timestamp = int(time.time())
            filename = f"recording_{timestamp}.wav"
            filepath = os.path.join(self.voice_dir, filename)
            
            with open(filepath, "wb") as f:
                f.write(audio.get_wav_data())
            
            return {
                "success": True,
                "filepath": filepath,
                "filename": filename,
                "duration": duration,
                "language": language
            }
            
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "录音超时"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def transcribe_audio(self, audio_file: str, language: str = None) -> Dict[str, Any]:
        """转录音频文件"""
        try:
            if language is None:
                language = settings.SPEECH_RECOGNITION_LANGUAGE
            
            # 读取音频文件
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
            
            # 识别语音
            try:
                # 尝试使用Google语音识别
                text = self.recognizer.recognize_google(audio, language=language)
                confidence = 0.8  # Google不提供置信度
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "error": "无法识别语音内容"
                }
            except sr.RequestError as e:
                return {
                    "success": False,
                    "error": f"语音识别服务错误: {e}"
                }
            
            return {
                "success": True,
                "text": text,
                "confidence": confidence,
                "language": language,
                "audio_file": audio_file
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def transcribe_microphone(self, duration: int = 5, language: str = None) -> Dict[str, Any]:
        """从麦克风实时转录"""
        try:
            if language is None:
                language = settings.SPEECH_RECOGNITION_LANGUAGE
            
            # 调整环境噪音
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            
            # 监听并转录
            print("请说话...")
            audio = self.recognizer.listen(source, timeout=duration, phrase_time_limit=duration)
            
            # 识别语音
            try:
                text = self.recognizer.recognize_google(audio, language=language)
                confidence = 0.8
            except sr.UnknownValueError:
                return {
                    "success": False,
                    "error": "无法识别语音内容"
                }
            except sr.RequestError as e:
                return {
                    "success": False,
                    "error": f"语音识别服务错误: {e}"
                }
            
            return {
                "success": True,
                "text": text,
                "confidence": confidence,
                "language": language,
                "duration": duration
            }
            
        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "录音超时"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def text_to_speech(self, text: str, language: str = None, save_file: bool = False) -> Dict[str, Any]:
        """文本转语音"""
        try:
            if language is None:
                language = settings.SPEECH_SYNTHESIS_LANGUAGE
            
            # 设置语言
            if language.startswith('zh'):
                self.tts_engine.setProperty('rate', 120)  # 中文语速稍慢
            else:
                self.tts_engine.setProperty('rate', 150)  # 英文语速
            
            if save_file:
                # 保存为音频文件
                timestamp = int(time.time())
                filename = f"tts_{timestamp}.wav"
                filepath = os.path.join(self.voice_dir, filename)
                
                self.tts_engine.save_to_file(text, filepath)
                self.tts_engine.runAndWait()
                
                return {
                    "success": True,
                    "text": text,
                    "filepath": filepath,
                    "filename": filename,
                    "language": language
                }
            else:
                # 直接播放
                self.tts_engine.say(text)
                self.tts_engine.runAndWait()
                
                return {
                    "success": True,
                    "text": text,
                    "language": language,
                    "played": True
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_available_languages(self) -> Dict[str, Any]:
        """获取可用的语音识别语言"""
        languages = {
            "zh-CN": "中文（简体）",
            "zh-TW": "中文（繁体）",
            "en-US": "英语（美国）",
            "en-GB": "英语（英国）",
            "ja-JP": "日语",
            "ko-KR": "韩语",
            "fr-FR": "法语",
            "de-DE": "德语",
            "es-ES": "西班牙语",
            "ru-RU": "俄语"
        }
        
        return {
            "success": True,
            "languages": languages
        }
    
    def get_voice_settings(self) -> Dict[str, Any]:
        """获取语音设置"""
        try:
            voices = self.tts_engine.getProperty('voices')
            current_voice = self.tts_engine.getProperty('voice')
            rate = self.tts_engine.getProperty('rate')
            volume = self.tts_engine.getProperty('volume')
            
            return {
                "success": True,
                "current_voice": current_voice,
                "rate": rate,
                "volume": volume,
                "available_voices": [
                    {
                        "id": voice.id,
                        "name": voice.name,
                        "languages": voice.languages
                    }
                    for voice in voices
                ]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def set_voice_settings(self, voice_id: str = None, rate: int = None, volume: float = None) -> Dict[str, Any]:
        """设置语音参数"""
        try:
            if voice_id:
                self.tts_engine.setProperty('voice', voice_id)
            
            if rate:
                self.tts_engine.setProperty('rate', rate)
            
            if volume is not None:
                self.tts_engine.setProperty('volume', volume)
            
            return {
                "success": True,
                "message": "语音设置已更新"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def analyze_audio_quality(self, audio_file: str) -> Dict[str, Any]:
        """分析音频质量"""
        try:
            # 读取音频文件
            with wave.open(audio_file, 'rb') as wav_file:
                frames = wav_file.readframes(-1)
                sample_rate = wav_file.getframerate()
                channels = wav_file.getnchannels()
                sample_width = wav_file.getsampwidth()
                duration = wav_file.getnframes() / sample_rate
            
            # 转换为numpy数组
            audio_data = np.frombuffer(frames, dtype=np.int16)
            
            # 计算音频质量指标
            rms = np.sqrt(np.mean(audio_data**2))  # 均方根
            max_amplitude = np.max(np.abs(audio_data))  # 最大振幅
            snr = 20 * np.log10(max_amplitude / (rms + 1e-10))  # 信噪比
            
            # 检测静音段
            silence_threshold = rms * 0.1
            silence_frames = np.sum(np.abs(audio_data) < silence_threshold)
            silence_ratio = silence_frames / len(audio_data)
            
            return {
                "success": True,
                "sample_rate": sample_rate,
                "channels": channels,
                "sample_width": sample_width,
                "duration": duration,
                "rms": float(rms),
                "max_amplitude": int(max_amplitude),
                "snr": float(snr),
                "silence_ratio": float(silence_ratio),
                "quality_score": min(100, max(0, 100 - silence_ratio * 100))
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }