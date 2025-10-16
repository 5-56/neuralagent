# 认证测试
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from main import app
from core.database import get_db, Base
from models.user import User
from services.auth_service import AuthService

# 测试数据库
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as c:
        yield c
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module")
def auth_service():
    return AuthService()

def test_register_user(client):
    """测试用户注册"""
    user_data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "testpassword123",
        "display_name": "Test User"
    }
    
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]
    assert "id" in data

def test_register_duplicate_user(client):
    """测试重复用户注册"""
    user_data = {
        "username": "testuser2",
        "email": "test2@example.com",
        "password": "testpassword123"
    }
    
    # 第一次注册
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 201
    
    # 第二次注册相同用户
    response = client.post("/api/v1/auth/register", json=user_data)
    assert response.status_code == 400

def test_login_user(client):
    """测试用户登录"""
    # 先注册用户
    user_data = {
        "username": "testuser3",
        "email": "test3@example.com",
        "password": "testpassword123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    # 登录
    login_data = {
        "username": "testuser3",
        "password": "testpassword123"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client):
    """测试无效凭据登录"""
    login_data = {
        "username": "nonexistent",
        "password": "wrongpassword"
    }
    
    response = client.post("/api/v1/auth/login", data=login_data)
    assert response.status_code == 401

def test_get_current_user(client):
    """测试获取当前用户信息"""
    # 先注册并登录
    user_data = {
        "username": "testuser4",
        "email": "test4@example.com",
        "password": "testpassword123"
    }
    client.post("/api/v1/auth/register", json=user_data)
    
    login_data = {
        "username": "testuser4",
        "password": "testpassword123"
    }
    login_response = client.post("/api/v1/auth/login", data=login_data)
    token = login_response.json()["access_token"]
    
    # 获取用户信息
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/v1/auth/me", headers=headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["username"] == user_data["username"]
    assert data["email"] == user_data["email"]

def test_auth_service_password_hashing(auth_service):
    """测试密码哈希"""
    password = "testpassword123"
    hashed = auth_service.get_password_hash(password)
    
    assert hashed != password
    assert auth_service.verify_password(password, hashed)
    assert not auth_service.verify_password("wrongpassword", hashed)

def test_auth_service_token_creation(auth_service):
    """测试令牌创建和验证"""
    data = {"sub": "testuser"}
    token = auth_service.create_access_token(data)
    
    # 验证令牌
    token_data = auth_service.verify_access_token(token)
    assert token_data.username == "testuser"

def test_auth_service_refresh_token(auth_service):
    """测试刷新令牌"""
    data = {"sub": "testuser"}
    refresh_token = auth_service.create_refresh_token(data)
    
    # 验证刷新令牌
    token_data = auth_service.verify_refresh_token(refresh_token)
    assert token_data.username == "testuser"