"""
Settings module for SmartWebBot.

Handles configuration management, persistence, and validation for all system settings.
"""

from .models import (
    PlusIntegrationSettings,
    RmaProcessingSettings,
    NotificationSettings,
    PerformanceSettings,
    SystemSettings
)

from .service import SettingsService
from .router import settings_router

__all__ = [
    'PlusIntegrationSettings',
    'RmaProcessingSettings', 
    'NotificationSettings',
    'PerformanceSettings',
    'SystemSettings',
    'SettingsService',
    'settings_router'
]
