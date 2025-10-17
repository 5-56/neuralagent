# 文件相关数据模型
from sqlalchemy import Column, String, Text, Integer, Boolean, DateTime, ForeignKey, JSON, Enum, BigInteger
from sqlalchemy.orm import relationship
from enum import Enum as PyEnum
from .base import BaseModel, SoftDeleteMixin

class FileType(PyEnum):
    """文件类型枚举"""
    IMAGE = "image"
    DOCUMENT = "document"
    AUDIO = "audio"
    VIDEO = "video"
    ARCHIVE = "archive"
    CODE = "code"
    DATA = "data"
    OTHER = "other"

class FileStatus(PyEnum):
    """文件状态枚举"""
    UPLOADING = "uploading"
    UPLOADED = "uploaded"
    PROCESSING = "processing"
    PROCESSED = "processed"
    ERROR = "error"
    DELETED = "deleted"

class File(BaseModel, SoftDeleteMixin):
    """文件模型"""
    __tablename__ = "files"
    
    # 基本信息
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # 文件信息
    file_size = Column(BigInteger, nullable=False)  # 文件大小（字节）
    file_path = Column(String(500), nullable=False)  # 文件路径
    file_hash = Column(String(64), nullable=True)  # 文件哈希值
    
    # 状态信息
    status = Column(Enum(FileStatus), default=FileStatus.UPLOADED, nullable=False)
    is_public = Column(Boolean, default=False, nullable=False)
    
    # 元数据
    metadata = Column(JSON, nullable=True)
    tags = Column(JSON, nullable=True)  # 文件标签
    
    # 处理信息
    processing_config = Column(JSON, nullable=True)
    processing_result = Column(JSON, nullable=True)
    error_message = Column(Text, nullable=True)
    
    # 访问信息
    download_count = Column(Integer, default=0, nullable=False)
    last_accessed = Column(DateTime(timezone=True), nullable=True)
    
    # 外键
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    user = relationship("User")
    uploads = relationship("FileUpload", back_populates="file", cascade="all, delete-orphan")

class FileUpload(BaseModel):
    """文件上传记录模型"""
    __tablename__ = "file_uploads"
    
    # 基本信息
    upload_id = Column(String(100), unique=True, nullable=False)
    status = Column(Enum(FileStatus), default=FileStatus.UPLOADING, nullable=False)
    
    # 文件信息
    filename = Column(String(255), nullable=False)
    file_size = Column(BigInteger, nullable=False)
    file_type = Column(Enum(FileType), nullable=False)
    mime_type = Column(String(100), nullable=False)
    
    # 上传信息
    upload_progress = Column(Integer, default=0, nullable=False)  # 上传进度 0-100
    chunk_count = Column(Integer, nullable=True)  # 分片数量
    uploaded_chunks = Column(Integer, default=0, nullable=False)  # 已上传分片数
    
    # 配置信息
    upload_config = Column(JSON, nullable=True)
    metadata = Column(JSON, nullable=True)
    
    # 时间信息
    started_at = Column(DateTime(timezone=True), nullable=False)
    completed_at = Column(DateTime(timezone=True), nullable=True)
    expires_at = Column(DateTime(timezone=True), nullable=True)  # 过期时间
    
    # 错误信息
    error_message = Column(Text, nullable=True)
    error_details = Column(JSON, nullable=True)
    
    # 外键
    file_id = Column(Integer, ForeignKey("files.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 关系
    file = relationship("File", back_populates="uploads")
    user = relationship("User")