#!/bin/bash

# 羲和 (Xihe) 桌面应用安装脚本
# 支持 Windows (WSL)、macOS 和 Linux

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查命令是否存在
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# 检查操作系统
detect_os() {
    if [[ "$OSTYPE" == "linux-gnu"* ]]; then
        if command_exists apt-get; then
            echo "ubuntu"
        elif command_exists yum; then
            echo "centos"
        elif command_exists pacman; then
            echo "arch"
        else
            echo "linux"
        fi
    elif [[ "$OSTYPE" == "darwin"* ]]; then
        echo "macos"
    elif [[ "$OSTYPE" == "msys" ]] || [[ "$OSTYPE" == "cygwin" ]]; then
        echo "windows"
    else
        echo "unknown"
    fi
}

# 安装系统依赖
install_system_deps() {
    local os=$(detect_os)
    
    log_info "检测到操作系统: $os"
    
    case $os in
        "ubuntu"|"debian")
            log_info "安装系统依赖..."
            sudo apt-get update
            sudo apt-get install -y \
                python3 python3-pip python3-venv \
                nodejs npm \
                postgresql postgresql-contrib \
                redis-server \
                build-essential \
                libpq-dev \
                libffi-dev \
                libssl-dev \
                libjpeg-dev \
                libpng-dev \
                libgl1-mesa-glx \
                libglib2.0-0 \
                libsm6 \
                libxext6 \
                libxrender-dev \
                libgomp1
            ;;
        "centos"|"rhel"|"fedora")
            log_info "安装系统依赖..."
            sudo yum update -y
            sudo yum install -y \
                python3 python3-pip \
                nodejs npm \
                postgresql postgresql-server \
                redis \
                gcc gcc-c++ \
                postgresql-devel \
                libffi-devel \
                openssl-devel \
                libjpeg-turbo-devel \
                libpng-devel \
                mesa-libGL \
                glib2 \
                libSM \
                libXext \
                libXrender
            ;;
        "arch")
            log_info "安装系统依赖..."
            sudo pacman -Syu --noconfirm
            sudo pacman -S --noconfirm \
                python python-pip \
                nodejs npm \
                postgresql \
                redis \
                base-devel \
                postgresql-libs \
                libffi \
                openssl \
                libjpeg-turbo \
                libpng \
                mesa \
                glib2 \
                libsm \
                libxext \
                libxrender
            ;;
        "macos")
            log_info "检查 Homebrew..."
            if ! command_exists brew; then
                log_info "安装 Homebrew..."
                /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
            fi
            
            log_info "安装系统依赖..."
            brew install python@3.11 node postgresql redis
            ;;
        "windows")
            log_warning "Windows 用户请使用 WSL 或手动安装依赖"
            log_info "推荐使用 WSL2 + Ubuntu 20.04+"
            ;;
        *)
            log_error "不支持的操作系统: $os"
            exit 1
            ;;
    esac
}

# 检查Python版本
check_python() {
    if command_exists python3; then
        local version=$(python3 --version 2>&1 | cut -d' ' -f2)
        local major=$(echo $version | cut -d'.' -f1)
        local minor=$(echo $version | cut -d'.' -f2)
        
        if [ "$major" -eq 3 ] && [ "$minor" -ge 9 ]; then
            log_success "Python 版本检查通过: $version"
            return 0
        else
            log_error "Python 版本过低: $version (需要 3.9+)"
            return 1
        fi
    else
        log_error "未找到 Python3"
        return 1
    fi
}

# 检查Node.js版本
check_nodejs() {
    if command_exists node; then
        local version=$(node --version | cut -d'v' -f2)
        local major=$(echo $version | cut -d'.' -f1)
        
        if [ "$major" -ge 18 ]; then
            log_success "Node.js 版本检查通过: $version"
            return 0
        else
            log_error "Node.js 版本过低: $version (需要 18+)"
            return 1
        fi
    else
        log_error "未找到 Node.js"
        return 1
    fi
}

# 设置数据库
setup_database() {
    local os=$(detect_os)
    
    log_info "设置数据库..."
    
    case $os in
        "ubuntu"|"debian"|"centos"|"rhel"|"fedora"|"arch")
            sudo systemctl start postgresql
            sudo systemctl enable postgresql
            
            # 创建数据库和用户
            sudo -u postgres psql -c "CREATE DATABASE xihe;" || true
            sudo -u postgres psql -c "CREATE USER xihe WITH PASSWORD 'xihe_password';" || true
            sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE xihe TO xihe;" || true
            ;;
        "macos")
            brew services start postgresql
            
            # 创建数据库和用户
            createdb xihe || true
            psql -d xihe -c "CREATE USER xihe WITH PASSWORD 'xihe_password';" || true
            psql -d xihe -c "GRANT ALL PRIVILEGES ON DATABASE xihe TO xihe;" || true
            ;;
    esac
    
    log_success "数据库设置完成"
}

# 设置Redis
setup_redis() {
    local os=$(detect_os)
    
    log_info "设置 Redis..."
    
    case $os in
        "ubuntu"|"debian"|"centos"|"rhel"|"fedora"|"arch")
            sudo systemctl start redis
            sudo systemctl enable redis
            ;;
        "macos")
            brew services start redis
            ;;
    esac
    
    log_success "Redis 设置完成"
}

# 安装后端依赖
install_backend() {
    log_info "安装后端依赖..."
    
    cd backend
    
    # 创建虚拟环境
    python3 -m venv venv
    
    # 激活虚拟环境
    source venv/bin/activate
    
    # 升级pip
    pip install --upgrade pip
    
    # 安装依赖
    pip install -r requirements.txt
    
    # 复制环境配置文件
    if [ ! -f .env ]; then
        cp .env.example .env
        log_warning "请编辑 backend/.env 文件配置您的API密钥"
    fi
    
    cd ..
    
    log_success "后端依赖安装完成"
}

# 安装前端依赖
install_frontend() {
    log_info "安装前端依赖..."
    
    cd frontend
    
    # 安装依赖
    npm install
    
    # 复制环境配置文件
    if [ ! -f .env ]; then
        cp .env.example .env
    fi
    
    cd ..
    
    log_success "前端依赖安装完成"
}

# 创建启动脚本
create_start_scripts() {
    log_info "创建启动脚本..."
    
    # 后端启动脚本
    cat > start_backend.sh << 'EOF'
#!/bin/bash
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
EOF
    
    # 前端启动脚本
    cat > start_frontend.sh << 'EOF'
#!/bin/bash
cd frontend
npm run electron-dev
EOF
    
    # 完整启动脚本
    cat > start_xihe.sh << 'EOF'
#!/bin/bash
echo "启动羲和桌面应用..."

# 启动后端
cd backend
source venv/bin/activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# 等待后端启动
sleep 5

# 启动前端
cd ../frontend
npm run electron-dev &
FRONTEND_PID=$!

# 等待用户中断
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT
wait
EOF
    
    chmod +x start_backend.sh start_frontend.sh start_xihe.sh
    
    log_success "启动脚本创建完成"
}

# 主安装函数
main() {
    echo "=========================================="
    echo "    羲和 (Xihe) 桌面应用安装程序"
    echo "=========================================="
    echo
    
    # 检查系统要求
    log_info "检查系统要求..."
    
    if ! check_python; then
        log_error "Python 检查失败"
        exit 1
    fi
    
    if ! check_nodejs; then
        log_error "Node.js 检查失败"
        exit 1
    fi
    
    # 安装系统依赖
    install_system_deps
    
    # 设置数据库
    setup_database
    
    # 设置Redis
    setup_redis
    
    # 安装后端
    install_backend
    
    # 安装前端
    install_frontend
    
    # 创建启动脚本
    create_start_scripts
    
    echo
    echo "=========================================="
    log_success "安装完成！"
    echo "=========================================="
    echo
    echo "下一步："
    echo "1. 编辑 backend/.env 文件，配置您的API密钥"
    echo "2. 运行 ./start_xihe.sh 启动应用"
    echo
    echo "或者分别启动："
    echo "- 后端: ./start_backend.sh"
    echo "- 前端: ./start_frontend.sh"
    echo
    echo "文档: https://github.com/your-org/xihe"
    echo "问题反馈: https://github.com/your-org/xihe/issues"
    echo
}

# 运行主函数
main "$@"