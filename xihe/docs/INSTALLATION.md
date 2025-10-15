# 羲和 (Xihe) 安装指南

## 系统要求

### 最低要求
- **操作系统**: Windows 10+, macOS 10.15+, Ubuntu 20.04+
- **Python**: 3.9 或更高版本
- **Node.js**: 18 或更高版本
- **内存**: 4GB RAM
- **存储**: 2GB 可用空间
- **网络**: 稳定的互联网连接（用于AI服务）

### 推荐配置
- **操作系统**: Windows 11, macOS 12+, Ubuntu 22.04+
- **Python**: 3.11
- **Node.js**: 20 LTS
- **内存**: 8GB RAM 或更多
- **存储**: 5GB 可用空间
- **GPU**: 支持CUDA的显卡（用于本地AI模型）

## 快速安装

### 自动安装（推荐）

1. **克隆项目**
```bash
git clone https://github.com/your-org/xihe.git
cd xihe
```

2. **运行安装脚本**
```bash
# Linux/macOS
chmod +x install.sh
./install.sh

# Windows (WSL)
bash install.sh
```

3. **配置API密钥**
```bash
# 编辑后端配置文件
nano backend/.env

# 至少配置一个AI提供商的API密钥
OPENAI_API_KEY=your-openai-api-key
# 或
ANTHROPIC_API_KEY=your-anthropic-api-key
```

4. **启动应用**
```bash
./start_xihe.sh
```

### 手动安装

#### 1. 安装系统依赖

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv nodejs npm postgresql redis-server
```

**CentOS/RHEL/Fedora:**
```bash
sudo yum install python3 python3-pip nodejs npm postgresql redis
# 或使用 dnf (Fedora)
sudo dnf install python3 python3-pip nodejs npm postgresql redis
```

**macOS:**
```bash
# 安装 Homebrew (如果未安装)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 安装依赖
brew install python@3.11 node postgresql redis
```

**Windows:**
```bash
# 使用 Chocolatey
choco install python nodejs postgresql redis

# 或使用 Scoop
scoop install python nodejs postgresql redis
```

#### 2. 设置数据库

**PostgreSQL:**
```bash
# 启动服务
sudo systemctl start postgresql  # Linux
brew services start postgresql   # macOS

# 创建数据库
sudo -u postgres psql
CREATE DATABASE xihe;
CREATE USER xihe WITH PASSWORD 'xihe_password';
GRANT ALL PRIVILEGES ON DATABASE xihe TO xihe;
\q
```

**Redis:**
```bash
# 启动服务
sudo systemctl start redis  # Linux
brew services start redis   # macOS
```

#### 3. 安装后端

```bash
cd backend

# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置您的API密钥

# 运行数据库迁移
alembic upgrade head

# 启动后端服务
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

#### 4. 安装前端

```bash
cd frontend

# 安装依赖
npm install

# 配置环境变量
cp .env.example .env

# 启动开发服务器
npm run electron-dev
```

## Docker 安装

### 使用 Docker Compose（推荐）

1. **克隆项目**
```bash
git clone https://github.com/your-org/xihe.git
cd xihe
```

2. **配置环境变量**
```bash
cp backend/.env.example backend/.env
# 编辑 backend/.env 文件
```

3. **启动服务**
```bash
docker-compose up -d
```

4. **访问应用**
- 前端: http://localhost:3000
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

### 单独构建镜像

**后端镜像:**
```bash
cd backend
docker build -t xihe-backend .
docker run -p 8000:8000 xihe-backend
```

**前端镜像:**
```bash
cd frontend
docker build -t xihe-frontend .
docker run -p 3000:3000 xihe-frontend
```

## 配置说明

### 环境变量配置

**后端配置 (`backend/.env`):**
```env
# 基础配置
DEBUG=true
SECRET_KEY=your-secret-key
DATABASE_URL=postgresql://xihe:xihe_password@localhost:5432/xihe
REDIS_URL=redis://localhost:6379

# AI提供商配置（至少配置一个）
OPENAI_API_KEY=your-openai-api-key
ANTHROPIC_API_KEY=your-anthropic-api-key
GOOGLE_API_KEY=your-google-api-key

# 可选配置
OLLAMA_BASE_URL=http://localhost:11434
AZURE_OPENAI_ENDPOINT=your-azure-endpoint
AZURE_OPENAI_API_KEY=your-azure-api-key
```

**前端配置 (`frontend/.env`):**
```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_WS_URL=ws://localhost:8000
```

### AI提供商配置

#### OpenAI
1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 创建API密钥
3. 在 `.env` 文件中设置 `OPENAI_API_KEY`

#### Anthropic
1. 访问 [Anthropic Console](https://console.anthropic.com/)
2. 创建API密钥
3. 在 `.env` 文件中设置 `ANTHROPIC_API_KEY`

#### Google Gemini
1. 访问 [Google AI Studio](https://makersuite.google.com/)
2. 创建API密钥
3. 在 `.env` 文件中设置 `GOOGLE_API_KEY`

#### 本地模型 (Ollama)
1. 安装 [Ollama](https://ollama.ai/)
2. 下载模型: `ollama pull llama2`
3. 在 `.env` 文件中设置 `OLLAMA_BASE_URL`

## 故障排除

### 常见问题

**1. Python版本问题**
```bash
# 检查Python版本
python3 --version

# 如果版本过低，安装Python 3.9+
# Ubuntu/Debian
sudo apt install python3.11

# macOS
brew install python@3.11
```

**2. Node.js版本问题**
```bash
# 检查Node.js版本
node --version

# 如果版本过低，安装Node.js 18+
# 使用nvm管理Node.js版本
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
nvm install 20
nvm use 20
```

**3. 数据库连接问题**
```bash
# 检查PostgreSQL状态
sudo systemctl status postgresql

# 检查数据库连接
psql -h localhost -U xihe -d xihe

# 重置数据库
sudo -u postgres psql -c "DROP DATABASE IF EXISTS xihe;"
sudo -u postgres psql -c "CREATE DATABASE xihe;"
```

**4. Redis连接问题**
```bash
# 检查Redis状态
sudo systemctl status redis

# 测试Redis连接
redis-cli ping
```

**5. 端口占用问题**
```bash
# 检查端口占用
lsof -i :8000  # 后端端口
lsof -i :3000  # 前端端口

# 杀死占用进程
kill -9 <PID>
```

### 日志查看

**后端日志:**
```bash
# 查看实时日志
tail -f backend/xihe.log

# 或查看Docker日志
docker-compose logs -f backend
```

**前端日志:**
```bash
# 查看Electron日志
npm run electron-dev

# 或查看Docker日志
docker-compose logs -f frontend
```

### 性能优化

**1. 数据库优化**
```sql
-- 创建索引
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_created_at ON tasks(created_at);

-- 分析查询性能
EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = 1;
```

**2. Redis优化**
```bash
# 配置Redis内存限制
echo "maxmemory 256mb" >> /etc/redis/redis.conf
echo "maxmemory-policy allkeys-lru" >> /etc/redis/redis.conf
```

**3. 应用优化**
```bash
# 启用生产模式
export NODE_ENV=production
export DEBUG=false

# 使用PM2管理进程
npm install -g pm2
pm2 start ecosystem.config.js
```

## 卸载

### 完全卸载

```bash
# 停止所有服务
docker-compose down  # 如果使用Docker

# 删除数据库
sudo -u postgres psql -c "DROP DATABASE xihe;"
sudo -u postgres psql -c "DROP USER xihe;"

# 删除项目文件
rm -rf /path/to/xihe

# 删除系统依赖（可选）
sudo apt remove python3-pip nodejs npm postgresql redis-server  # Ubuntu
brew uninstall python@3.11 node postgresql redis  # macOS
```

### 保留数据卸载

```bash
# 备份数据库
pg_dump -h localhost -U xihe xihe > xihe_backup.sql

# 停止服务
docker-compose down

# 删除应用文件
rm -rf /path/to/xihe

# 恢复数据（重新安装后）
psql -h localhost -U xihe xihe < xihe_backup.sql
```

## 支持

如果您在安装过程中遇到问题，请：

1. 查看 [常见问题](FAQ.md)
2. 搜索 [GitHub Issues](https://github.com/your-org/xihe/issues)
3. 创建新的 Issue 描述您的问题
4. 加入我们的 [Discord 社区](https://discord.gg/xihe)

## 更新

### 自动更新
```bash
# 拉取最新代码
git pull origin main

# 更新依赖
cd backend && pip install -r requirements.txt
cd ../frontend && npm install

# 重启服务
docker-compose restart
```

### 手动更新
```bash
# 备份当前版本
cp -r xihe xihe_backup_$(date +%Y%m%d)

# 拉取新版本
git pull origin main

# 运行数据库迁移
cd backend
alembic upgrade head

# 重启服务
./start_xihe.sh
```