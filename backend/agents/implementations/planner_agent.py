# 规划代理实现
import json
from typing import Dict, List, Any, Optional
from agents.core.agent import BaseAgent, AgentType, AgentStatus, AgentContext, AgentMessage
from core.ai_providers import AIProvider

class PlannerAgent(BaseAgent):
    """规划代理 - 负责任务分解和规划"""
    
    def __init__(self, ai_provider: AIProvider):
        super().__init__(
            agent_type=AgentType.PLANNER,
            ai_provider=ai_provider,
            name="PlannerAgent",
            description="智能任务规划代理，负责将复杂任务分解为可执行的步骤"
        )
    
    async def process_message(self, message: AgentMessage, context: AgentContext) -> AgentMessage:
        """处理消息"""
        try:
            self.set_status(AgentStatus.RUNNING)
            
            # 构建规划提示
            prompt = self._build_planning_prompt(message, context)
            
            # 调用AI生成规划
            messages = [{"role": "user", "content": prompt}]
            response = await self.ai_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=2048
            )
            
            # 解析响应
            plan = self._parse_planning_response(response)
            
            # 创建响应消息
            response_message = AgentMessage(
                role="assistant",
                content=json.dumps(plan, ensure_ascii=False, indent=2),
                metadata={
                    "agent_type": self.agent_type.value,
                    "plan": plan,
                    "confidence": plan.get("confidence", 0.8)
                }
            )
            
            self.set_status(AgentStatus.IDLE)
            return response_message
            
        except Exception as e:
            self.set_status(AgentStatus.ERROR)
            return AgentMessage(
                role="assistant",
                content=f"规划失败: {str(e)}",
                metadata={"error": str(e), "agent_type": self.agent_type.value}
            )
    
    def _build_planning_prompt(self, message: AgentMessage, context: AgentContext) -> str:
        """构建规划提示"""
        task_description = message.content
        
        prompt = f"""
你是一个智能任务规划代理。请分析以下任务并制定详细的执行计划。

任务描述: {task_description}

当前环境信息:
- 操作系统: {context.get('os', 'Unknown')}
- 运行应用: {', '.join(context.get('running_apps', []))}
- 屏幕分辨率: {context.get('screen_resolution', 'Unknown')}

请按照以下格式输出规划结果:

{{
    "task_analysis": {{
        "complexity": "low|medium|high",
        "estimated_duration": "预估执行时间（分钟）",
        "required_tools": ["需要的工具列表"],
        "potential_risks": ["潜在风险列表"]
    }},
    "execution_plan": {{
        "steps": [
            {{
                "step_id": "步骤ID",
                "step_name": "步骤名称",
                "description": "步骤描述",
                "action_type": "动作类型",
                "action_config": {{"具体配置"}},
                "dependencies": ["依赖的步骤ID"],
                "estimated_time": "预估时间（秒）",
                "success_criteria": "成功标准"
            }}
        ]
    }},
    "monitoring": {{
        "checkpoints": ["检查点列表"],
        "error_handling": "错误处理策略",
        "rollback_plan": "回滚计划"
    }},
    "confidence": 0.8
}}

请确保规划详细、可执行，并考虑各种异常情况。
"""
        return prompt
    
    def _parse_planning_response(self, response: str) -> Dict[str, Any]:
        """解析规划响应"""
        try:
            # 尝试直接解析JSON
            plan = json.loads(response)
            return plan
        except json.JSONDecodeError:
            # 如果直接解析失败，尝试提取JSON部分
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                try:
                    plan = json.loads(json_match.group())
                    return plan
                except json.JSONDecodeError:
                    pass
            
            # 如果都失败了，返回默认结构
            return {
                "task_analysis": {
                    "complexity": "medium",
                    "estimated_duration": "未知",
                    "required_tools": [],
                    "potential_risks": []
                },
                "execution_plan": {
                    "steps": [
                        {
                            "step_id": "step_1",
                            "step_name": "分析任务",
                            "description": "分析任务需求",
                            "action_type": "analyze",
                            "action_config": {},
                            "dependencies": [],
                            "estimated_time": 30,
                            "success_criteria": "理解任务要求"
                        }
                    ]
                },
                "monitoring": {
                    "checkpoints": [],
                    "error_handling": "重试或人工干预",
                    "rollback_plan": "停止执行"
                },
                "confidence": 0.5,
                "raw_response": response
            }
    
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """分析任务复杂度"""
        prompt = f"""
请分析以下任务的复杂度:

任务: {task_description}

请从以下维度分析:
1. 技术复杂度 (1-10)
2. 时间复杂度 (1-10) 
3. 资源需求 (1-10)
4. 风险等级 (1-10)
5. 技能要求 (1-10)

输出格式:
{{
    "technical_complexity": 5,
    "time_complexity": 6,
    "resource_requirements": 4,
    "risk_level": 3,
    "skill_requirements": 7,
    "overall_complexity": "medium",
    "recommendations": ["建议1", "建议2"]
}}
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self.ai_provider.generate_response(
            messages=messages,
            temperature=0.3,
            max_tokens=512
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return {
                "technical_complexity": 5,
                "time_complexity": 5,
                "resource_requirements": 5,
                "risk_level": 5,
                "skill_requirements": 5,
                "overall_complexity": "medium",
                "recommendations": ["需要进一步分析"]
            }
    
    async def optimize_plan(self, plan: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """优化规划"""
        prompt = f"""
请根据以下反馈优化任务规划:

原始规划:
{json.dumps(plan, ensure_ascii=False, indent=2)}

反馈:
{feedback}

请输出优化后的规划，保持JSON格式。
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self.ai_provider.generate_response(
            messages=messages,
            temperature=0.5,
            max_tokens=2048
        )
        
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            return plan