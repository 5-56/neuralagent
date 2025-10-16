# AI代理测试
import pytest
from unittest.mock import Mock, AsyncMock
from agents.core.agent import AgentType, AgentStatus, AgentContext, AgentMessage
from agents.implementations.planner_agent import PlannerAgent
from agents.implementations.executor_agent import ExecutorAgent
from core.ai_providers import AIProvider

@pytest.fixture
def mock_ai_provider():
    """模拟AI提供商"""
    provider = Mock(spec=AIProvider)
    provider.generate_response = AsyncMock(return_value='{"test": "response"}')
    return provider

@pytest.fixture
def planner_agent(mock_ai_provider):
    """规划代理实例"""
    return PlannerAgent(mock_ai_provider)

@pytest.fixture
def executor_agent(mock_ai_provider):
    """执行代理实例"""
    return ExecutorAgent(mock_ai_provider)

@pytest.fixture
def sample_context():
    """示例上下文"""
    return AgentContext(
        os="Windows",
        running_apps=["notepad.exe", "chrome.exe"],
        screen_resolution="1920x1080"
    )

@pytest.fixture
def sample_message():
    """示例消息"""
    return AgentMessage(
        role="user",
        content="打开记事本并输入一些文本",
        metadata={"task_type": "desktop_automation"}
    )

class TestPlannerAgent:
    """规划代理测试"""
    
    def test_planner_agent_initialization(self, planner_agent):
        """测试规划代理初始化"""
        assert planner_agent.agent_type == AgentType.PLANNER
        assert planner_agent.name == "PlannerAgent"
        assert planner_agent.status == AgentStatus.IDLE
    
    @pytest.mark.asyncio
    async def test_process_message_success(self, planner_agent, sample_message, sample_context):
        """测试处理消息成功"""
        response = await planner_agent.process_message(sample_message, sample_context)
        
        assert response.role == "assistant"
        assert "task_analysis" in response.content
        assert "execution_plan" in response.content
        assert planner_agent.status == AgentStatus.IDLE
    
    @pytest.mark.asyncio
    async def test_process_message_error(self, planner_agent, sample_message, sample_context):
        """测试处理消息错误"""
        # 模拟AI提供商抛出异常
        planner_agent.ai_provider.generate_response.side_effect = Exception("AI服务错误")
        
        response = await planner_agent.process_message(sample_message, sample_context)
        
        assert response.role == "assistant"
        assert "规划失败" in response.content
        assert planner_agent.status == AgentStatus.ERROR
    
    @pytest.mark.asyncio
    async def test_analyze_task_complexity(self, planner_agent):
        """测试任务复杂度分析"""
        task_description = "创建一个复杂的自动化脚本"
        
        result = await planner_agent.analyze_task_complexity(task_description)
        
        assert "technical_complexity" in result
        assert "time_complexity" in result
        assert "overall_complexity" in result
        assert "recommendations" in result
    
    def test_build_planning_prompt(self, planner_agent, sample_message, sample_context):
        """测试构建规划提示"""
        prompt = planner_agent._build_planning_prompt(sample_message, sample_context)
        
        assert "任务描述" in prompt
        assert sample_message.content in prompt
        assert "操作系统" in prompt
        assert sample_context.os in prompt
    
    def test_parse_planning_response_valid_json(self, planner_agent):
        """测试解析有效的JSON响应"""
        valid_json = '{"task_analysis": {"complexity": "medium"}, "execution_plan": {"steps": []}}'
        
        result = planner_agent._parse_planning_response(valid_json)
        
        assert result["task_analysis"]["complexity"] == "medium"
        assert "execution_plan" in result
    
    def test_parse_planning_response_invalid_json(self, planner_agent):
        """测试解析无效的JSON响应"""
        invalid_json = "这不是有效的JSON"
        
        result = planner_agent._parse_planning_response(invalid_json)
        
        assert "task_analysis" in result
        assert "execution_plan" in result
        assert result["confidence"] == 0.5

class TestExecutorAgent:
    """执行代理测试"""
    
    def test_executor_agent_initialization(self, executor_agent):
        """测试执行代理初始化"""
        assert executor_agent.agent_type == AgentType.EXECUTOR
        assert executor_agent.name == "ExecutorAgent"
        assert executor_agent.status == AgentStatus.IDLE
    
    @pytest.mark.asyncio
    async def test_process_message_success(self, executor_agent, sample_message, sample_context):
        """测试处理消息成功"""
        # 模拟消息内容为JSON格式的动作数据
        sample_message.content = '{"action_type": "click", "coordinates": [100, 200]}'
        
        response = await executor_agent.process_message(sample_message, sample_context)
        
        assert response.role == "assistant"
        assert "action_type" in response.content
        assert executor_agent.status == AgentStatus.IDLE
    
    @pytest.mark.asyncio
    async def test_execute_click_action(self, executor_agent, sample_context):
        """测试执行点击动作"""
        action_data = {
            "action_type": "click",
            "coordinates": [100, 200]
        }
        
        result = await executor_agent._execute_action(action_data, sample_context)
        
        assert "success" in result
        assert result["action_type"] == "click"
    
    @pytest.mark.asyncio
    async def test_execute_type_action(self, executor_agent, sample_context):
        """测试执行输入动作"""
        action_data = {
            "action_type": "type",
            "text": "Hello World"
        }
        
        result = await executor_agent._execute_action(action_data, sample_context)
        
        assert "success" in result
        assert result["action_type"] == "type"
        assert result["text"] == "Hello World"
    
    @pytest.mark.asyncio
    async def test_execute_scroll_action(self, executor_agent, sample_context):
        """测试执行滚动动作"""
        action_data = {
            "action_type": "scroll",
            "direction": "down",
            "amount": 3
        }
        
        result = await executor_agent._execute_action(action_data, sample_context)
        
        assert "success" in result
        assert result["action_type"] == "scroll"
        assert result["direction"] == "down"
    
    @pytest.mark.asyncio
    async def test_execute_screenshot_action(self, executor_agent, sample_context):
        """测试执行截图动作"""
        action_data = {
            "action_type": "screenshot"
        }
        
        result = await executor_agent._execute_action(action_data, sample_context)
        
        assert "success" in result
        assert result["action_type"] == "screenshot"
    
    @pytest.mark.asyncio
    async def test_execute_wait_action(self, executor_agent, sample_context):
        """测试执行等待动作"""
        action_data = {
            "action_type": "wait",
            "duration": 1
        }
        
        result = await executor_agent._execute_action(action_data, sample_context)
        
        assert result["success"] is True
        assert result["action_type"] == "wait"
        assert result["duration"] == 1
    
    def test_parse_action_data_json(self, executor_agent):
        """测试解析JSON格式的动作数据"""
        json_data = '{"action_type": "click", "coordinates": [100, 200]}'
        
        result = executor_agent._parse_action_data(json_data)
        
        assert result["action_type"] == "click"
        assert result["coordinates"] == [100, 200]
    
    def test_parse_action_data_natural_language(self, executor_agent):
        """测试解析自然语言指令"""
        instruction = "点击屏幕上的按钮"
        
        result = executor_agent._parse_action_data(instruction)
        
        assert result["action_type"] == "click"
        assert "点击" in result["description"]
    
    def test_parse_action_data_type_instruction(self, executor_agent):
        """测试解析输入指令"""
        instruction = "在输入框中输入文本"
        
        result = executor_agent._parse_action_data(instruction)
        
        assert result["action_type"] == "type"
        assert "输入" in result["description"]
    
    def test_parse_action_data_scroll_instruction(self, executor_agent):
        """测试解析滚动指令"""
        instruction = "向下滚动页面"
        
        result = executor_agent._parse_action_data(instruction)
        
        assert result["action_type"] == "scroll"
        assert "滚动" in result["description"]