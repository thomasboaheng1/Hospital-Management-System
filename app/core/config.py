from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Hospital Management System"
    VERSION: str = "2.0.0"
    
    # Server Configuration
    HOST: str = Field(default="0.0.0.0", description="Server host")
    PORT: int = Field(default=8000, description="Server port")
    DEBUG: bool = Field(default=True, description="Debug mode")
    
    # Database Configuration
    DATABASE_URL: str = Field(
        default="sqlite:///./hospital.db",
        description="Database connection URL"
    )
    
    # Security Configuration
    SECRET_KEY: str = Field(
        default="your-super-secret-key-here-change-in-production",
        description="Secret key for JWT tokens"
    )
    ALGORITHM: str = Field(default="HS256", description="JWT algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=30,
        description="Access token expiration time in minutes"
    )
    REFRESH_TOKEN_EXPIRE_DAYS: int = Field(
        default=7,
        description="Refresh token expiration time in days"
    )
    
    # CORS Configuration
    CORS_ORIGINS: List[str] = Field(
        default=[
            "http://localhost:3000",
            "http://localhost:3001",
            "http://localhost:8001",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:3001",
            "http://127.0.0.1:8001",
            "http://localhost:*",
            "http://127.0.0.1:*"
        ],
        description="Allowed CORS origins"
    )
    
    # Email Configuration
    SMTP_TLS: bool = Field(default=True, description="Use TLS for SMTP")
    SMTP_PORT: int = Field(default=587, description="SMTP port")
    SMTP_HOST: str = Field(default="smtp.gmail.com", description="SMTP host")
    SMTP_USER: str = Field(default="your-email@gmail.com", description="SMTP username")
    SMTP_PASSWORD: str = Field(default="your-app-password", description="SMTP password")
    
    # File Upload Configuration
    UPLOAD_DIR: str = Field(default="uploads", description="Upload directory")
    MAX_FILE_SIZE: int = Field(
        default=5 * 1024 * 1024,  # 5MB
        description="Maximum file size in bytes"
    )
    ALLOWED_FILE_TYPES: List[str] = Field(
        default=[".jpg", ".jpeg", ".png", ".pdf", ".doc", ".docx"],
        description="Allowed file types for uploads"
    )
    
    # Hospital Information
    HOSPITAL_NAME: str = Field(
        default="City General Hospital",
        description="Hospital name"
    )
    HOSPITAL_ADDRESS: str = Field(
        default="123 Healthcare Street, Medical City",
        description="Hospital address"
    )
    HOSPITAL_PHONE: str = Field(
        default="+1-555-0123",
        description="Hospital phone number"
    )
    HOSPITAL_EMAIL: str = Field(
        default="info@cityhospital.com",
        description="Hospital email"
    )
    
    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60,
        description="Rate limit requests per minute"
    )
    
    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format"
    )
    
    # Cache Configuration
    CACHE_TTL: int = Field(
        default=300,  # 5 minutes
        description="Cache time to live in seconds"
    )
    
    @validator("SECRET_KEY")
    def validate_secret_key(cls, v):
        if v == "your-super-secret-key-here-change-in-production":
            print("⚠️  Warning: Using default secret key. Change this in production!")
        return v
    
    @validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if v.startswith("sqlite:///"):
            # Ensure the database directory exists
            db_path = Path(v.replace("sqlite:///", ""))
            db_path.parent.mkdir(parents=True, exist_ok=True)
        return v
    
    @property
    def is_development(self) -> bool:
        return self.DEBUG
    
    @property
    def is_production(self) -> bool:
        return not self.DEBUG
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        env_file_encoding = "utf-8"

settings = Settings() 