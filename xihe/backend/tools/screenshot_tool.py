# 截图工具
import os
import time
from typing import Optional, Dict, Any, List, Tuple
from PIL import Image
import mss
import cv2
import numpy as np

class ScreenshotTool:
    """截图工具类"""
    
    def __init__(self):
        self.screenshot_dir = "screenshots"
        self._ensure_screenshot_dir()
    
    def _ensure_screenshot_dir(self):
        """确保截图目录存在"""
        if not os.path.exists(self.screenshot_dir):
            os.makedirs(self.screenshot_dir)
    
    def capture_screen(self, region: Optional[Dict[str, int]] = None) -> Dict[str, Any]:
        """捕获屏幕截图"""
        try:
            with mss.mss() as sct:
                if region:
                    # 捕获指定区域
                    monitor = {
                        "top": region.get("top", 0),
                        "left": region.get("left", 0),
                        "width": region.get("width", 1920),
                        "height": region.get("height", 1080)
                    }
                else:
                    # 捕获整个屏幕
                    monitor = sct.monitors[1]  # 主显示器
                
                # 截图
                screenshot = sct.grab(monitor)
                
                # 转换为PIL Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                
                # 保存截图
                timestamp = int(time.time())
                filename = f"screenshot_{timestamp}.png"
                filepath = os.path.join(self.screenshot_dir, filename)
                img.save(filepath)
                
                return {
                    "success": True,
                    "filepath": filepath,
                    "filename": filename,
                    "size": screenshot.size,
                    "region": region or "full_screen"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def capture_window(self, window_title: str) -> Dict[str, Any]:
        """捕获指定窗口"""
        try:
            # 这里需要实现窗口捕获逻辑
            # 暂时使用全屏截图
            return self.capture_screen()
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def find_element_by_image(self, template_path: str, screenshot_path: Optional[str] = None) -> Dict[str, Any]:
        """通过图像模板查找元素"""
        try:
            if screenshot_path is None:
                # 先截图
                screenshot_result = self.capture_screen()
                if not screenshot_result["success"]:
                    return screenshot_result
                screenshot_path = screenshot_result["filepath"]
            
            # 读取图像
            screenshot = cv2.imread(screenshot_path)
            template = cv2.imread(template_path)
            
            if screenshot is None or template is None:
                return {
                    "success": False,
                    "error": "无法读取图像文件"
                }
            
            # 模板匹配
            result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 设置匹配阈值
            threshold = 0.8
            if max_val >= threshold:
                # 计算中心点
                h, w = template.shape[:2]
                center_x = max_loc[0] + w // 2
                center_y = max_loc[1] + h // 2
                
                return {
                    "success": True,
                    "found": True,
                    "confidence": float(max_val),
                    "coordinates": (center_x, center_y),
                    "bounding_box": {
                        "x": max_loc[0],
                        "y": max_loc[1],
                        "width": w,
                        "height": h
                    }
                }
            else:
                return {
                    "success": True,
                    "found": False,
                    "confidence": float(max_val),
                    "message": "未找到匹配的元素"
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def detect_ui_elements(self, screenshot_path: str) -> Dict[str, Any]:
        """检测UI元素"""
        try:
            # 读取图像
            image = cv2.imread(screenshot_path)
            if image is None:
                return {
                    "success": False,
                    "error": "无法读取截图文件"
                }
            
            # 转换为灰度图
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            
            # 检测边缘
            edges = cv2.Canny(gray, 50, 150)
            
            # 查找轮廓
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            # 过滤轮廓
            elements = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 100:  # 过滤小元素
                    x, y, w, h = cv2.boundingRect(contour)
                    elements.append({
                        "type": "rectangle",
                        "coordinates": (x + w//2, y + h//2),
                        "bounding_box": {"x": x, "y": y, "width": w, "height": h},
                        "area": area
                    })
            
            return {
                "success": True,
                "elements": elements,
                "element_count": len(elements)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def compare_screenshots(self, img1_path: str, img2_path: str) -> Dict[str, Any]:
        """比较两张截图"""
        try:
            # 读取图像
            img1 = cv2.imread(img1_path)
            img2 = cv2.imread(img2_path)
            
            if img1 is None or img2 is None:
                return {
                    "success": False,
                    "error": "无法读取图像文件"
                }
            
            # 确保图像尺寸相同
            if img1.shape != img2.shape:
                img2 = cv2.resize(img2, (img1.shape[1], img1.shape[0]))
            
            # 计算差异
            diff = cv2.absdiff(img1, img2)
            gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
            
            # 计算相似度
            similarity = 1 - (np.sum(gray_diff) / (gray_diff.shape[0] * gray_diff.shape[1] * 255))
            
            # 查找变化区域
            _, thresh = cv2.threshold(gray_diff, 30, 255, cv2.THRESH_BINARY)
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            changes = []
            for contour in contours:
                area = cv2.contourArea(contour)
                if area > 50:  # 过滤小变化
                    x, y, w, h = cv2.boundingRect(contour)
                    changes.append({
                        "coordinates": (x + w//2, y + h//2),
                        "bounding_box": {"x": x, "y": y, "width": w, "height": h},
                        "area": area
                    })
            
            return {
                "success": True,
                "similarity": float(similarity),
                "changes": changes,
                "change_count": len(changes)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_screen_info(self) -> Dict[str, Any]:
        """获取屏幕信息"""
        try:
            with mss.mss() as sct:
                monitors = sct.monitors
                
                screen_info = {
                    "monitor_count": len(monitors) - 1,  # 减去虚拟显示器
                    "monitors": []
                }
                
                for i, monitor in enumerate(monitors[1:], 1):  # 跳过虚拟显示器
                    screen_info["monitors"].append({
                        "id": i,
                        "width": monitor["width"],
                        "height": monitor["height"],
                        "left": monitor["left"],
                        "top": monitor["top"]
                    })
                
                return {
                    "success": True,
                    "screen_info": screen_info
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }