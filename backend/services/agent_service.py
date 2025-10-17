# AI代理服务
from typing import Dict, Any, Optional
from models.task import TaskStep
from core.ai_providers import AIProviderManager
from agents.implementations.planner_agent import PlannerAgent
from agents.implementations.executor_agent import ExecutorAgent

class AgentService:
    """AI代理服务"""
    
    def __init__(self):
        self.ai_provider_manager = AIProviderManager()
        self.planner_agent = None
        self.executor_agent = None
    
    async def get_planner_agent(self) -> PlannerAgent:
        """获取规划代理"""
        if not self.planner_agent:
            ai_provider = await self.ai_provider_manager.get_provider("openai")
            self.planner_agent = PlannerAgent(ai_provider)
        return self.planner_agent
    
    async def get_executor_agent(self) -> ExecutorAgent:
        """获取执行代理"""
        if not self.executor_agent:
            ai_provider = await self.ai_provider_manager.get_provider("openai")
            self.executor_agent = ExecutorAgent(ai_provider)
        return self.executor_agent
    
    async def execute_task_step(self, step: TaskStep) -> Dict[str, Any]:
        """执行任务步骤"""
        try:
            executor_agent = await self.get_executor_agent()
            
            # 构建执行上下文
            context = {
                "step_id": step.id,
                "step_name": step.step_name,
                "action_type": step.action_type,
                "action_config": step.action_config or {},
                "input_data": step.input_data or {}
            }
            
            # 执行步骤
            result = await executor_agent.execute_workflow_step(step, context)
            
            return {
                "success": result.get("success", False),
                "output_data": result.get("result_data"),
                "error": result.get("error"),
                "execution_time": result.get("execution_time", 0)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "execution_time": 0
            }
    
    async def plan_task(self, task_description: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """规划任务"""
        try:
            planner_agent = await self.get_planner_agent()
            
            # 创建规划消息
            from agents.core.agent import AgentMessage, AgentContext
            message = AgentMessage(
                role="user",
                content=task_description,
                metadata={"task_type": "planning"}
            )
            
            agent_context = AgentContext(**context)
            
            # 执行规划
            response = await planner_agent.process_message(message, agent_context)
            
            return {
                "success": True,
                "plan": response.metadata.get("plan", {}),
                "confidence": response.metadata.get("confidence", 0.8)
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "plan": {}
            }
    
    async def analyze_task_complexity(self, task_description: str) -> Dict[str, Any]:
        """分析任务复杂度"""
        try:
            planner_agent = await self.get_planner_agent()
            result = await planner_agent.analyze_task_complexity(task_description)
            return result
        except Exception as e:
            return {
                "technical_complexity": 5,
                "time_complexity": 5,
                "resource_requirements": 5,
                "risk_level": 5,
                "skill_requirements": 5,
                "overall_complexity": "medium",
                "recommendations": ["需要进一步分析"],
                "error": str(e)
            }
    
    async def optimize_plan(self, plan: Dict[str, Any], feedback: str) -> Dict[str, Any]:
        """优化规划"""
        try:
            planner_agent = await self.get_planner_agent()
            result = await planner_agent.optimize_plan(plan, feedback)
            return result
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "optimized_plan": plan
            }
    
    async def get_agent_status(self) -> Dict[str, Any]:
        """获取代理状态"""
        status = {
            "planner_agent": {
                "available": self.planner_agent is not None,
                "status": self.planner_agent.status.value if self.planner_agent else "unavailable"
            },
            "executor_agent": {
                "available": self.executor_agent is not None,
                "status": self.executor_agent.status.value if self.executor_agent else "unavailable"
            },
            "ai_providers": await self.ai_provider_manager.get_available_providers()
        }
        
        return status