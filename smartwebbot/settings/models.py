"""
Pydantic models for settings validation and type safety.
"""

from typing import Optional, Literal, Union
from pydantic import BaseModel, Field, validator, HttpUrl
from enum import Enum


class LogLevel(str, Enum):
    """Log level enumeration."""
    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"


class NotificationLevel(str, Enum):
    """Notification level enumeration."""
    ALL = "all"
    IMPORTANT = "important"
    CRITICAL = "critical"


class PlusIntegrationSettings(BaseModel):
    """PLUS system integration settings."""
    base_url: Union[HttpUrl, str] = Field(default="https://plus.reconext.com", description="PLUS system base URL")
    username: str = Field(default="", description="PLUS username")
    password: str = Field(default="", description="PLUS password")
    api_key: Optional[str] = Field(default="", description="Optional API key")
    timeout: int = Field(default=30, ge=5, le=300, description="Connection timeout in seconds")
    retry_attempts: int = Field(default=3, ge=0, le=10, description="Number of retry attempts")
    enabled: bool = Field(default=True, description="Enable PLUS integration")
    
    @validator('base_url', pre=True)
    def validate_base_url(cls, v):
        """Allow both string and HttpUrl types."""
        if isinstance(v, str):
            return v
        return str(v)
    
    class Config:
        json_schema_extra = {
            "example": {
                "base_url": "https://plus.reconext.com",
                "username": "admin",
                "password": "password123",
                "api_key": "optional-api-key",
                "timeout": 30,
                "retry_attempts": 3,
                "enabled": True
            }
        }


class RmaProcessingSettings(BaseModel):
    """RMA processing configuration settings."""
    auto_processing: bool = Field(default=True, description="Enable automatic processing")
    batch_size: int = Field(default=100, ge=1, le=1000, description="Number of RMAs to process per batch")
    tracking_validation: bool = Field(default=True, description="Enable tracking number validation")
    label_generation: bool = Field(default=True, description="Enable automatic label generation")
    quality_checks: bool = Field(default=True, description="Enable quality checks")
    max_processing_time: int = Field(default=30, ge=1, le=120, description="Max processing time in minutes")
    error_retry_count: int = Field(default=999, ge=0, le=9999, description="Number of retries on error (999=unlimited)")
    
    class Config:
        json_schema_extra = {
            "example": {
                "auto_processing": True,
                "batch_size": 100,
                "tracking_validation": True,
                "label_generation": True,
                "quality_checks": True,
                "max_processing_time": 30,
                "error_retry_count": 3
            }
        }


class NotificationSettings(BaseModel):
    """Notification system settings."""
    email_notifications: bool = Field(default=True, description="Enable email notifications")
    sms_notifications: bool = Field(default=False, description="Enable SMS notifications")
    push_notifications: bool = Field(default=True, description="Enable push notifications")
    email_address: Optional[str] = Field(default="", description="Email address for notifications")
    phone_number: Optional[str] = Field(default="", description="Phone number for SMS")
    notification_level: NotificationLevel = Field(default=NotificationLevel.IMPORTANT, description="Notification level")
    
    @validator('email_address')
    def validate_email(cls, v):
        if v and '@' not in v:
            raise ValueError('Invalid email address format')
        return v
    
    @validator('phone_number')
    def validate_phone(cls, v):
        if v and not v.replace('+', '').replace('-', '').replace('(', '').replace(')', '').replace(' ', '').isdigit():
            raise ValueError('Invalid phone number format')
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "email_notifications": True,
                "sms_notifications": False,
                "push_notifications": True,
                "email_address": "admin@company.com",
                "phone_number": "+1-555-123-4567",
                "notification_level": "important"
            }
        }


class PerformanceSettings(BaseModel):
    """System performance and monitoring settings."""
    enable_caching: bool = Field(default=True, description="Enable system caching")
    enable_logging: bool = Field(default=True, description="Enable detailed logging")
    log_level: LogLevel = Field(default=LogLevel.INFO, description="Logging level")
    max_concurrent_tasks: int = Field(default=5, ge=1, le=20, description="Maximum concurrent tasks")
    task_timeout: int = Field(default=300, ge=30, le=3600, description="Task timeout in seconds")
    cache_size: int = Field(default=100, ge=10, le=1000, description="Cache size in MB")
    memory_threshold: int = Field(default=80, ge=50, le=95, description="Memory usage threshold percentage")
    
    class Config:
        json_schema_extra = {
            "example": {
                "enable_caching": True,
                "enable_logging": True,
                "log_level": "info",
                "max_concurrent_tasks": 5,
                "task_timeout": 300,
                "cache_size": 100,
                "memory_threshold": 80
            }
        }


class SystemSettings(BaseModel):
    """Complete system settings container."""
    plus_integration: PlusIntegrationSettings = Field(default_factory=PlusIntegrationSettings)
    rma_processing: RmaProcessingSettings = Field(default_factory=RmaProcessingSettings)
    notifications: NotificationSettings = Field(default_factory=NotificationSettings)
    performance: PerformanceSettings = Field(default_factory=PerformanceSettings)
    
    class Config:
        json_schema_extra = {
            "example": {
                "plus_integration": PlusIntegrationSettings.Config.json_schema_extra["example"],
                "rma_processing": RmaProcessingSettings.Config.json_schema_extra["example"],
                "notifications": NotificationSettings.Config.json_schema_extra["example"],
                "performance": PerformanceSettings.Config.json_schema_extra["example"]
            }
        }


# Request/Response models for API endpoints
class PlusConnectionTestRequest(BaseModel):
    """Request model for testing PLUS connection."""
    base_url: Union[HttpUrl, str]
    username: str
    password: str
    api_key: Optional[str] = ""
    
    @validator('base_url', pre=True)
    def validate_base_url(cls, v):
        """Allow both string and HttpUrl types."""
        if isinstance(v, str):
            return v
        return str(v)


class PlusConnectionTestResponse(BaseModel):
    """Response model for PLUS connection test."""
    success: bool
    message: str
    response_time: Optional[float] = None
    server_version: Optional[str] = None


class SettingsUpdateRequest(BaseModel):
    """Generic settings update request."""
    settings: dict


class SettingsUpdateResponse(BaseModel):
    """Generic settings update response."""
    success: bool
    message: str
    updated_fields: list[str] = []


class SettingsExportResponse(BaseModel):
    """Settings export response."""
    settings: SystemSettings
    export_timestamp: str
    version: str = "1.0"


class SettingsImportRequest(BaseModel):
    """Settings import request."""
    settings: SystemSettings
    overwrite_existing: bool = False
