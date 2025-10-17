# 羲和 (Xihe) - 智能化桌面助手

羲和是一个基于AI的智能化桌面自动化助手，相比NeuralAgent具有更强的智能化能力和更广泛的AI提供商支持。

## 🌟 核心特性

### 智能化增强
- **多模态交互**: 支持文本、语音、图像、手势等多种交互方式
- **上下文感知**: 深度理解用户意图和桌面环境状态
- **自适应学习**: 根据用户习惯优化操作策略
- **工作流编排**: 支持复杂任务的自动化编排和执行

### 广泛的AI提供商支持
- **主流云服务**: OpenAI GPT系列、Anthropic Claude、Google Gemini、Azure OpenAI
- **开源模型**: Ollama、LM Studio、vLLM等本地部署方案
- **专业模型**: 针对特定领域的专业AI模型
- **混合推理**: 支持多模型协同工作

### 高级功能
- **语音交互**: 实时语音识别和合成
- **文档处理**: PDF、Word、Excel等文档的智能处理
- **网页自动化**: 高级浏览器操作和数据提取
- **系统集成**: 深度集成操作系统API
- **安全保护**: 企业级安全控制和隐私保护

## 🏗️ 技术架构

```
xihe/
├── backend/              # FastAPI后端服务
│   ├── api/             # API路由
│   ├── core/            # 核心业务逻辑
│   ├── models/          # 数据模型
│   ├── services/        # 服务层
│   └── utils/           # 工具函数
├── frontend/            # Electron+React前端
│   ├── src/             # React应用源码
│   ├── electron/        # Electron主进程
│   └── public/          # 静态资源
├── agents/              # AI代理系统
│   ├── core/            # 代理核心
│   ├── providers/       # AI提供商适配
│   └── tools/           # 工具集
├── desktop/             # 桌面自动化
│   ├── automation/      # 自动化引擎
│   ├── ui/              # UI交互
│   └── system/          # 系统集成
└── docs/                # 文档
```

## 🚀 快速开始

### 环境要求
- Python 3.9+
- Node.js 18+
- PostgreSQL 13+
- 操作系统: Windows 10+, macOS 10.15+, Ubuntu 20.04+

### 安装步骤

1. **克隆项目**
```bash
git clone https://github.com/your-org/xihe.git
cd xihe
```

2. **后端设置**
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
alembic upgrade head
uvicorn main:app --reload
```

3. **前端设置**
```bash
cd frontend
npm install
npm run electron:dev
```

## 📖 使用指南

### 基本使用
1. 启动应用后，通过语音或文本输入任务描述
2. 羲和会分析任务并制定执行计划
3. 自动执行桌面操作，完成用户任务
4. 提供实时反馈和进度监控

### 高级功能
- **工作流设计**: 通过可视化界面设计复杂自动化流程
- **模型选择**: 根据任务类型选择最适合的AI模型
- **安全模式**: 在受控环境中执行敏感操作
- **团队协作**: 共享工作流和最佳实践

## 🔧 配置

### AI提供商配置
在 `backend/.env` 中配置AI提供商：

```env
# OpenAI
OPENAI_API_KEY=your_key
OPENAI_BASE_URL=https://api.openai.com/v1

# Anthropic
ANTHROPIC_API_KEY=your_key

# Google Gemini
GOOGLE_API_KEY=your_key

# 本地模型
OLLAMA_BASE_URL=http://localhost:11434
```

### 安全配置
```env
# 安全设置
SECURITY_LEVEL=high
ALLOWED_DOMAINS=*.example.com
ENCRYPTION_KEY=your_encryption_key
```

## 🤝 贡献指南

我们欢迎社区贡献！请查看 [CONTRIBUTING.md](CONTRIBUTING.md) 了解详细信息。

## 📄 许可证

本项目采用 MIT 许可证。详见 [LICENSE](LICENSE) 文件。

## 🆘 支持

- 📧 邮箱: support@xihe.ai
- 💬 讨论: [GitHub Discussions](https://github.com/your-org/xihe/discussions)
- 🐛 问题: [GitHub Issues](https://github.com/your-org/xihe/issues)

---

**羲和** - 让AI真正理解你的桌面世界