# 数据库连接和初始化
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool
from core.config import settings

logger = logging.getLogger(__name__)

# 创建数据库引擎
if settings.DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
        echo=settings.DEBUG
    )
else:
    engine = create_engine(
        settings.DATABASE_URL,
        pool_size=settings.DATABASE_POOL_SIZE,
        max_overflow=settings.DATABASE_MAX_OVERFLOW,
        echo=settings.DEBUG
    )

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基础模型类
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

def get_db() -> Session:
    """获取数据库会话"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def init_db():
    """初始化数据库"""
    try:
        # 导入所有模型以确保它们被注册
        from models import user, task, agent, workflow, conversation, file, settings as settings_model
        
        # 创建所有表
        Base.metadata.create_all(bind=engine)
        logger.info("数据库表创建成功")
        
        # 创建默认管理员用户
        await create_default_admin()
        
    except Exception as e:
        logger.error(f"数据库初始化失败: {e}")
        raise

async def create_default_admin():
    """创建默认管理员用户"""
    try:
        from services.auth_service import AuthService
        from models.user import User
        
        db = SessionLocal()
        try:
            # 检查是否已存在管理员用户
            admin_user = db.query(User).filter(User.username == "admin").first()
            if admin_user:
                logger.info("管理员用户已存在")
                return
            
            # 创建管理员用户
            auth_service = AuthService()
            admin_data = {
                "username": "admin",
                "email": "admin@xihe.ai",
                "password": "admin123456",
                "display_name": "系统管理员"
            }
            
            hashed_password = auth_service.get_password_hash(admin_data["password"])
            admin_user = User(
                username=admin_data["username"],
                email=admin_data["email"],
                hashed_password=hashed_password,
                is_active=True,
                is_verified=True,
                is_superuser=True
            )
            
            db.add(admin_user)
            db.commit()
            logger.info("默认管理员用户创建成功")
            
        finally:
            db.close()
            
    except Exception as e:
        logger.error(f"创建默认管理员用户失败: {e}")

def get_engine():
    """获取数据库引擎"""
    return engine