# 执行代理实现
import json
import asyncio
from typing import Dict, List, Any, Optional
from agents.core.agent import BaseAgent, AgentType, AgentStatus, AgentContext, AgentMessage
from core.ai_providers import AIProvider
from core.desktop_automation import DesktopAutomation, ActionType

class ExecutorAgent(BaseAgent):
    """执行代理 - 负责具体操作执行"""
    
    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            agent_type=AgentType.EXECUTOR,
            ai_provider=ai_provider,
            name="ExecutorAgent",
            description="智能执行代理，负责执行具体的桌面操作"
        )
        self.desktop_automation = DesktopAutomation()
    
    async def process_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """处理消息"""
        try:
            self.set_status(AgentStatus.RUNNING)
            
            # 解析执行指令
            action_data = self._parse_action_data(message.content)
            
            # 执行操作
            result = await self._execute_action(action_data, context)
            
            # 创建响应消息
            response_message = AgentMessage(
                role="assistant",
                content=json.dumps(result, ensure_ascii=False, indent=2),
                metadata={
                    "agent_type": self.agent_type.value,
                    "action_result": result,
                    "success": result.get("success", False)
                }
            )
            
            self.set_status(AgentStatus.IDLE)
            return response_message
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            return AgentMessage(
                role="assistant",
                content=f"执行失败: {str(e)}",
                metadata={"error": str(e), "agent_type": self.agent_type.value}
            )
    
    def _parse_action_data(self, content: str) -> Dict[str, Any]:
        """解析动作数据"""
        try:
            # 尝试解析JSON
            if content.startswith('{'):
                return json.loads(content)
            
            # 如果不是JSON，尝试解析为自然语言指令
            return self._parse_natural_language_instruction(content)
            
        except json.JSONDecodeError:
            return self._parse_natural_language_instruction(content)
    
    def _parse_natural_language_instruction(self, instruction: str) -> Dict[str, Any]:
        """解析自然语言指令"""
        # 这里可以使用AI来解析自然语言指令
        # 暂时返回简单的解析结果
        instruction_lower = instruction.lower()
        
        if "点击" in instruction or "click" in instruction_lower:
            return {
                "action_type": "click",
                "description": instruction,
                "coordinates": None,  # 需要AI分析确定坐标
                "element": None
            }
        elif "输入" in instruction or "type" in instruction_lower:
            return {
                "action_type": "type",
                "description": instruction,
                "text": None,  # 需要AI提取文本
                "target": None
            }
        elif "滚动" in instruction or "scroll" in instruction_lower:
            return {
                "action_type": "scroll",
                "description": instruction,
                "direction": "down",
                "amount": 3
            }
        else:
            return {
                "action_type": "unknown",
                "description": instruction,
                "raw_instruction": instruction
            }
    
    async def _execute_action(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行动作"""
        action_type = action_data.get("action_type", "unknown")
        
        try:
            if action_type == "click":
                return await self._execute_click(action_data, context)
            elif action_type == "type":
                return await self._execute_type(action_data, context)
            elif action_type == "scroll":
                return await self._execute_scroll(action_data, context)
            elif action_type == "screenshot":
                return await self._execute_screenshot(action_data, context)
            elif action_type == "wait":
                return await self._execute_wait(action_data, context)
            else:
                return await self._execute_unknown_action(action_data, context)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "action_type": action_type,
                "action_data": action_data
            }
    
    async def _execute_click(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行点击操作"""
        coordinates = action_data.get("coordinates")
        element = action_data.get("element")
        
        if coordinates:
            x, y = coordinates
            result = await self.desktop_automation.execute_action({
                "type": ActionType.CLICK,
                "params": {"x": x, "y": y}
            })
        elif element:
            # 需要先找到元素位置
            element_coords = await self._find_element_coordinates(element, context)
            if element_coords:
                result = await self.desktop_automation.execute_action({
                    "type": ActionType.CLICK,
                    "params": {"x": element_coords[0], "y": element_coords[1]}
                })
            else:
                return {
                    "success": False,
                    "error": "无法找到指定元素",
                    "element": element
                }
        else:
            return {
                "success": False,
                "error": "缺少点击坐标或元素信息"
            }
        
        return {
            "success": result.get("success", False),
            "action_type": "click",
            "coordinates": coordinates or element_coords,
            "result": result
        }
    
    async def _execute_type(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行输入操作"""
        text = action_data.get("text", "")
        target = action_data.get("target")
        
        if not text:
            return {
                "success": False,
                "error": "缺少输入文本"
            }
        
        # 如果指定了目标，先点击目标
        if target:
            target_coords = await self._find_element_coordinates(target, context)
            if target_coords:
                click_result = await self.desktop_automation.execute_action({
                    "type": ActionType.CLICK,
                    "params": {"x": target_coords[0], "y": target_coords[1]}
                })
                if not click_result.get("success", False):
                    return {
                        "success": False,
                        "error": "无法点击目标元素",
                        "target": target
                    }
        
        # 执行输入
        result = await self.desktop_automation.execute_action({
            "type": ActionType.TYPE,
            "params": {"text": text}
        })
        
        return {
            "success": result.get("success", False),
            "action_type": "type",
            "text": text,
            "target": target,
            "result": result
        }
    
    async def _execute_scroll(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行滚动操作"""
        direction = action_data.get("direction", "down")
        amount = action_data.get("amount", 3)
        
        result = await self.desktop_automation.execute_action({
            "type": ActionType.SCROLL,
            "params": {"direction": direction, "clicks": amount}
        })
        
        return {
            "success": result.get("success", False),
            "action_type": "scroll",
            "direction": direction,
            "amount": amount,
            "result": result
        }
    
    async def _execute_screenshot(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行截图操作"""
        result = await self.desktop_automation.execute_action({
            "type": ActionType.SCREENSHOT,
            "params": {}
        })
        
        return {
            "success": result.get("success", False),
            "action_type": "screenshot",
            "image_path": result.get("image_path"),
            "result": result
        }
    
    async def _execute_wait(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行等待操作"""
        duration = action_data.get("duration", 1)
        await asyncio.sleep(duration)
        
        return {
            "success": True,
            "action_type": "wait",
            "duration": duration
        }
    
    async def _execute_unknown_action(self, action_data: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行未知动作"""
        # 使用AI分析动作
        prompt = f"""
请分析以下动作指令并转换为可执行的操作:

指令: {action_data.get('description', '')}
原始数据: {json.dumps(action_data, ensure_ascii=False)}

请输出JSON格式的执行计划:
{{
    "action_type": "具体动作类型",
    "parameters": {{"参数": "值"}},
    "description": "动作描述",
    "confidence": 0.8
}}
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self.ai_provider.generate_response(
            messages=messages,
            temperature=0.3,
            max_tokens=512
        )
        
        try:
            ai_analysis = json.loads(response)
            # 根据AI分析执行动作
            return await self._execute_action(ai_analysis, context)
        except json.JSONDecodeError:
            return {
                "success": False,
                "error": "无法解析动作指令",
                "raw_instruction": action_data.get('description', ''),
                "ai_response": response
            }
    
    async def _find_element_coordinates(self, element_description: str, context: AgentContext) -> Optional[tuple]:
        """查找元素坐标"""
        # 这里应该实现元素识别逻辑
        # 暂时返回None，表示未找到
        return None
    
    async def execute_workflow_step(self, step: Dict[str, Any], context: AgentContext) -> Dict[str, Any]:
        """执行工作流步骤"""
        step_id = step.get("step_id", "unknown")
        step_name = step.get("step_name", "未知步骤")
        action_config = step.get("action_config", {})
        
        try:
            self.set_status(AgentStatus.RUNNING)
            
            # 执行步骤
            result = await self._execute_action(action_config, context)
            
            # 记录执行结果
            result.update({
                "step_id": step_id,
                "step_name": step_name,
                "execution_time": result.get("execution_time", 0)
            })
            
            self.set_status(AgentStatus.IDLE)
            return result
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            return {
                "success": False,
                "error": str(e),
                "step_id": step_id,
                "step_name": step_name
            }