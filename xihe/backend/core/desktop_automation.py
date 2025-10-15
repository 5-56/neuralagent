"""
桌面自动化核心模块
支持跨平台的桌面操作自动化
"""

import asyncio
import platform
import logging
from typing import Dict, List, Optional, Any, Tuple
from enum import Enum
import base64
from io import BytesIO

import pyautogui
import mss
from PIL import Image
import pyperclip
import psutil

from core.exceptions import DesktopAutomationError

logger = logging.getLogger(__name__)

# 设置pyautogui安全设置
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.1


class ActionType(str, Enum):
    """操作类型枚举"""
    CLICK = "click"
    DOUBLE_CLICK = "double_click"
    RIGHT_CLICK = "right_click"
    DRAG = "drag"
    SCROLL = "scroll"
    TYPE = "type"
    KEY = "key"
    KEY_COMBO = "key_combo"
    SCREENSHOT = "screenshot"
    WAIT = "wait"
    FOCUS_WINDOW = "focus_window"
    LAUNCH_APP = "launch_app"
    CLOSE_APP = "close_app"


class DesktopAutomation:
    """桌面自动化核心类"""
    
    def __init__(self):
        self.screen_width, self.screen_height = pyautogui.size()
        self.platform = platform.system().lower()
        logger.info(f"桌面自动化初始化完成，平台: {self.platform}, 屏幕分辨率: {self.screen_width}x{self.screen_height}")
    
    async def execute_action(self, action: Dict[str, Any]) -> Dict[str, Any]:
        """执行单个操作"""
        action_type = action.get("type")
        params = action.get("params", {})
        
        try:
            if action_type == ActionType.CLICK:
                return await self._click(params)
            elif action_type == ActionType.DOUBLE_CLICK:
                return await self._double_click(params)
            elif action_type == ActionType.RIGHT_CLICK:
                return await self._right_click(params)
            elif action_type == ActionType.DRAG:
                return await self._drag(params)
            elif action_type == ActionType.SCROLL:
                return await self._scroll(params)
            elif action_type == ActionType.TYPE:
                return await self._type(params)
            elif action_type == ActionType.KEY:
                return await self._key(params)
            elif action_type == ActionType.KEY_COMBO:
                return await self._key_combo(params)
            elif action_type == ActionType.SCREENSHOT:
                return await self._screenshot(params)
            elif action_type == ActionType.WAIT:
                return await self._wait(params)
            elif action_type == ActionType.FOCUS_WINDOW:
                return await self._focus_window(params)
            elif action_type == ActionType.LAUNCH_APP:
                return await self._launch_app(params)
            elif action_type == ActionType.CLOSE_APP:
                return await self._close_app(params)
            else:
                raise DesktopAutomationError(f"不支持的操作类型: {action_type}", action_type)
        
        except Exception as e:
            logger.error(f"执行操作失败: {action_type}, 错误: {e}")
            raise DesktopAutomationError(f"执行操作失败: {str(e)}", action_type)
    
    async def execute_actions(self, actions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """执行多个操作"""
        results = []
        for action in actions:
            result = await self.execute_action(action)
            results.append(result)
        return results
    
    async def _click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """点击操作"""
        x = params.get("x", 0)
        y = params.get("y", 0)
        button = params.get("button", "left")
        
        # 坐标验证
        x = max(0, min(x, self.screen_width - 1))
        y = max(0, min(y, self.screen_height - 1))
        
        pyautogui.click(x, y, button=button)
        
        return {
            "success": True,
            "action": "click",
            "coordinates": {"x": x, "y": y},
            "button": button
        }
    
    async def _double_click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """双击操作"""
        x = params.get("x", 0)
        y = params.get("y", 0)
        button = params.get("button", "left")
        
        x = max(0, min(x, self.screen_width - 1))
        y = max(0, min(y, self.screen_height - 1))
        
        pyautogui.doubleClick(x, y, button=button)
        
        return {
            "success": True,
            "action": "double_click",
            "coordinates": {"x": x, "y": y},
            "button": button
        }
    
    async def _right_click(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """右键点击操作"""
        x = params.get("x", 0)
        y = params.get("y", 0)
        
        x = max(0, min(x, self.screen_width - 1))
        y = max(0, min(y, self.screen_height - 1))
        
        pyautogui.rightClick(x, y)
        
        return {
            "success": True,
            "action": "right_click",
            "coordinates": {"x": x, "y": y}
        }
    
    async def _drag(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """拖拽操作"""
        start_x = params.get("start_x", 0)
        start_y = params.get("start_y", 0)
        end_x = params.get("end_x", 0)
        end_y = params.get("end_y", 0)
        duration = params.get("duration", 1.0)
        button = params.get("button", "left")
        
        # 坐标验证
        start_x = max(0, min(start_x, self.screen_width - 1))
        start_y = max(0, min(start_y, self.screen_height - 1))
        end_x = max(0, min(end_x, self.screen_width - 1))
        end_y = max(0, min(end_y, self.screen_height - 1))
        
        pyautogui.drag(end_x - start_x, end_y - start_y, duration=duration, button=button)
        
        return {
            "success": True,
            "action": "drag",
            "start_coordinates": {"x": start_x, "y": start_y},
            "end_coordinates": {"x": end_x, "y": end_y},
            "duration": duration
        }
    
    async def _scroll(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """滚动操作"""
        x = params.get("x", self.screen_width // 2)
        y = params.get("y", self.screen_height // 2)
        clicks = params.get("clicks", 3)
        direction = params.get("direction", "up")  # up, down, left, right
        
        x = max(0, min(x, self.screen_width - 1))
        y = max(0, min(y, self.screen_height - 1))
        
        # 移动到目标位置
        pyautogui.moveTo(x, y)
        
        # 执行滚动
        if direction == "up":
            pyautogui.scroll(clicks)
        elif direction == "down":
            pyautogui.scroll(-clicks)
        elif direction == "left":
            pyautogui.hscroll(-clicks)
        elif direction == "right":
            pyautogui.hscroll(clicks)
        
        return {
            "success": True,
            "action": "scroll",
            "coordinates": {"x": x, "y": y},
            "clicks": clicks,
            "direction": direction
        }
    
    async def _type(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """输入文本操作"""
        text = params.get("text", "")
        interval = params.get("interval", 0.05)
        clear_first = params.get("clear_first", False)
        
        if clear_first:
            # 全选并删除
            if self.platform == "darwin":
                pyautogui.hotkey("cmd", "a")
            else:
                pyautogui.hotkey("ctrl", "a")
            pyautogui.press("backspace")
        
        # 处理Unicode文本
        try:
            text.encode("ascii")
            # ASCII文本，直接输入
            pyautogui.write(text, interval=interval)
        except UnicodeEncodeError:
            # Unicode文本，使用剪贴板
            old_clipboard = pyperclip.paste()
            pyperclip.copy(text)
            await asyncio.sleep(0.1)  # 等待剪贴板更新
            
            if self.platform == "darwin":
                pyautogui.hotkey("cmd", "v")
            else:
                pyautogui.hotkey("ctrl", "v")
            
            await asyncio.sleep(0.1)
            pyperclip.copy(old_clipboard)  # 恢复原剪贴板内容
        
        return {
            "success": True,
            "action": "type",
            "text": text,
            "interval": interval
        }
    
    async def _key(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """按键操作"""
        key = params.get("key", "")
        presses = params.get("presses", 1)
        interval = params.get("interval", 0.1)
        
        pyautogui.press(key, presses=presses, interval=interval)
        
        return {
            "success": True,
            "action": "key",
            "key": key,
            "presses": presses
        }
    
    async def _key_combo(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """组合键操作"""
        keys = params.get("keys", [])
        interval = params.get("interval", 0.1)
        
        if not keys:
            raise DesktopAutomationError("组合键不能为空", "key_combo")
        
        pyautogui.hotkey(*keys)
        
        return {
            "success": True,
            "action": "key_combo",
            "keys": keys
        }
    
    async def _screenshot(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """截图操作"""
        region = params.get("region")  # {"x": 0, "y": 0, "width": 100, "height": 100}
        format_type = params.get("format", "png")
        quality = params.get("quality", 95)
        
        with mss.mss() as sct:
            if region:
                monitor = {
                    "top": region.get("y", 0),
                    "left": region.get("x", 0),
                    "width": region.get("width", self.screen_width),
                    "height": region.get("height", self.screen_height)
                }
            else:
                monitor = sct.monitors[1]  # 主显示器
            
            screenshot = sct.grab(monitor)
            img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
            
            # 转换为base64
            buffer = BytesIO()
            if format_type.lower() == "png":
                img.save(buffer, format="PNG")
            elif format_type.lower() == "jpeg":
                img.save(buffer, format="JPEG", quality=quality)
            else:
                img.save(buffer, format="PNG")
            
            img_base64 = base64.b64encode(buffer.getvalue()).decode("utf-8")
        
        return {
            "success": True,
            "action": "screenshot",
            "format": format_type,
            "data": img_base64,
            "region": region
        }
    
    async def _wait(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """等待操作"""
        duration = params.get("duration", 1.0)
        
        await asyncio.sleep(duration)
        
        return {
            "success": True,
            "action": "wait",
            "duration": duration
        }
    
    async def _focus_window(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """聚焦窗口操作"""
        window_title = params.get("window_title", "")
        app_name = params.get("app_name", "")
        
        if not window_title and not app_name:
            raise DesktopAutomationError("必须指定窗口标题或应用名称", "focus_window")
        
        # 这里需要根据平台实现不同的窗口聚焦逻辑
        # 简化实现，实际需要更复杂的窗口管理
        success = False
        
        if self.platform == "darwin":
            # macOS实现
            import subprocess
            try:
                if app_name:
                    subprocess.run(["osascript", "-e", f'tell application "{app_name}" to activate'], check=True)
                    success = True
            except subprocess.CalledProcessError:
                pass
        elif self.platform == "windows":
            # Windows实现
            try:
                import win32gui
                import win32con
                
                def enum_windows_callback(hwnd, windows):
                    if win32gui.IsWindowVisible(hwnd):
                        title = win32gui.GetWindowText(hwnd)
                        if window_title.lower() in title.lower() or app_name.lower() in title.lower():
                            windows.append(hwnd)
                
                windows = []
                win32gui.EnumWindows(enum_windows_callback, windows)
                
                if windows:
                    win32gui.SetForegroundWindow(windows[0])
                    success = True
            except ImportError:
                logger.warning("win32gui未安装，无法执行窗口聚焦操作")
        
        return {
            "success": success,
            "action": "focus_window",
            "window_title": window_title,
            "app_name": app_name
        }
    
    async def _launch_app(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """启动应用操作"""
        app_name = params.get("app_name", "")
        app_path = params.get("app_path", "")
        
        if not app_name and not app_path:
            raise DesktopAutomationError("必须指定应用名称或路径", "launch_app")
        
        success = False
        
        try:
            if app_path:
                # 使用指定路径启动
                import subprocess
                subprocess.Popen(app_path)
                success = True
            elif app_name:
                # 使用应用名称启动
                if self.platform == "darwin":
                    import subprocess
                    subprocess.Popen(["open", "-a", app_name])
                    success = True
                elif self.platform == "windows":
                    import subprocess
                    subprocess.Popen(["start", app_name], shell=True)
                    success = True
                elif self.platform == "linux":
                    import subprocess
                    subprocess.Popen([app_name])
                    success = True
        except Exception as e:
            logger.error(f"启动应用失败: {e}")
        
        return {
            "success": success,
            "action": "launch_app",
            "app_name": app_name,
            "app_path": app_path
        }
    
    async def _close_app(self, params: Dict[str, Any]) -> Dict[str, Any]:
        """关闭应用操作"""
        app_name = params.get("app_name", "")
        pid = params.get("pid")
        
        success = False
        
        try:
            if pid:
                # 通过PID关闭进程
                process = psutil.Process(pid)
                process.terminate()
                success = True
            elif app_name:
                # 通过应用名称关闭
                for proc in psutil.process_iter(['pid', 'name']):
                    if app_name.lower() in proc.info['name'].lower():
                        proc.terminate()
                        success = True
                        break
        except Exception as e:
            logger.error(f"关闭应用失败: {e}")
        
        return {
            "success": success,
            "action": "close_app",
            "app_name": app_name,
            "pid": pid
        }
    
    def get_screen_info(self) -> Dict[str, Any]:
        """获取屏幕信息"""
        return {
            "width": self.screen_width,
            "height": self.screen_height,
            "platform": self.platform
        }
    
    def get_running_apps(self) -> List[Dict[str, Any]]:
        """获取正在运行的应用列表"""
        apps = []
        try:
            for proc in psutil.process_iter(['pid', 'name', 'exe']):
                try:
                    app_info = {
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "exe": proc.info['exe']
                    }
                    apps.append(app_info)
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
        except Exception as e:
            logger.error(f"获取运行应用列表失败: {e}")
        
        return apps


# 全局桌面自动化实例
desktop_automation = DesktopAutomation()