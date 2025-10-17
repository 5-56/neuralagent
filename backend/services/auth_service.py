# 认证服务
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from core.config import settings
from models.user import User
from schemas.auth import UserCreate, TokenData

class AuthService:
    """认证服务"""
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.secret_key = settings.SECRET_KEY
        self.algorithm = settings.JWT_ALGORITHM
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """验证密码"""
        return self.pwd_context.verify(plain_password, hashed_password)
    
    def get_password_hash(self, password: str) -> str:
        """获取密码哈希"""
        return self.pwd_context.hash(password)
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建访问令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        
        to_encode.update({"exp": expire, "type": "access"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_refresh_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建刷新令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(days=7)
        
        to_encode.update({"exp": expire, "type": "refresh"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_email_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建邮箱验证令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=24)
        
        to_encode.update({"exp": expire, "type": "email"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def create_password_reset_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """创建密码重置令牌"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(hours=1)
        
        to_encode.update({"exp": expire, "type": "password_reset"})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str, token_type: str = "access") -> TokenData:
        """验证令牌"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            username: str = payload.get("sub")
            token_type_from_payload: str = payload.get("type")
            
            if username is None or token_type_from_payload != token_type:
                raise JWTError("Invalid token")
            
            return TokenData(username=username)
        except JWTError:
            raise JWTError("Invalid token")
    
    def verify_access_token(self, token: str) -> TokenData:
        """验证访问令牌"""
        return self.verify_token(token, "access")
    
    def verify_refresh_token(self, token: str) -> TokenData:
        """验证刷新令牌"""
        return self.verify_token(token, "refresh")
    
    def verify_email_token(self, token: str) -> TokenData:
        """验证邮箱令牌"""
        return self.verify_token(token, "email")
    
    def verify_password_reset_token(self, token: str) -> TokenData:
        """验证密码重置令牌"""
        return self.verify_token(token, "password_reset")
    
    async def create_user(self, db: Session, user_data: UserCreate) -> User:
        """创建用户"""
        # 检查用户是否已存在
        existing_user = db.query(User).filter(
            (User.email == user_data.email) | (User.username == user_data.username)
        ).first()
        
        if existing_user:
            raise ValueError("用户名或邮箱已存在")
        
        # 创建新用户
        hashed_password = self.get_password_hash(user_data.password)
        user = User(
            username=user_data.username,
            email=user_data.email,
            hashed_password=hashed_password,
            is_active=True,
            is_verified=False
        )
        
        db.add(user)
        db.commit()
        db.refresh(user)
        
        return user
    
    async def authenticate_user(self, db: Session, username: str, password: str) -> Optional[User]:
        """验证用户"""
        user = db.query(User).filter(
            (User.username == username) | (User.email == username)
        ).first()
        
        if not user:
            return None
        
        if not self.verify_password(password, user.hashed_password):
            return None
        
        if not user.is_active:
            return None
        
        return user
    
    async def get_current_user(self, db: Session, token: str) -> User:
        """获取当前用户"""
        try:
            token_data = self.verify_access_token(token)
            user = db.query(User).filter(User.username == token_data.username).first()
            
            if user is None:
                raise ValueError("用户不存在")
            
            return user
        except JWTError:
            raise ValueError("无效的令牌")