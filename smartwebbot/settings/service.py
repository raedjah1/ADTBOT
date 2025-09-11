"""
Settings service for business logic and operations.
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from datetime import datetime
import httpx

from .models import (
    SystemSettings,
    PlusIntegrationSettings,
    RmaProcessingSettings,
    NotificationSettings,
    PerformanceSettings,
    PlusConnectionTestRequest,
    PlusConnectionTestResponse
)
from .persistence import SettingsPersistence

logger = logging.getLogger(__name__)


class SettingsService:
    """Service class for managing system settings."""
    
    def __init__(self, settings_dir: str = "config"):
        """
        Initialize settings service.
        
        Args:
            settings_dir: Directory for settings storage
        """
        self.persistence = SettingsPersistence(settings_dir)
        self._current_settings: Optional[SystemSettings] = None
        self._settings_cache_time: Optional[datetime] = None
        self.cache_duration_seconds = 300  # 5 minutes
    
    def _get_cached_settings(self) -> Optional[SystemSettings]:
        """Get cached settings if still valid."""
        if (self._current_settings is None or 
            self._settings_cache_time is None or
            (datetime.now() - self._settings_cache_time).total_seconds() > self.cache_duration_seconds):
            return None
        return self._current_settings
    
    def _update_cache(self, settings: SystemSettings) -> None:
        """Update settings cache."""
        self._current_settings = settings
        self._settings_cache_time = datetime.now()
    
    def get_all_settings(self) -> SystemSettings:
        """
        Get all system settings.
        
        Returns:
            SystemSettings: Current system settings
        """
        # Check cache first
        cached_settings = self._get_cached_settings()
        if cached_settings:
            return cached_settings
        
        # Load from persistence
        settings = self.persistence.load_settings()
        self._update_cache(settings)
        return settings
    
    def get_plus_settings(self) -> PlusIntegrationSettings:
        """Get PLUS integration settings."""
        return self.get_all_settings().plus_integration
    
    def get_rma_settings(self) -> RmaProcessingSettings:
        """Get RMA processing settings."""
        return self.get_all_settings().rma_processing
    
    def get_notification_settings(self) -> NotificationSettings:
        """Get notification settings."""
        return self.get_all_settings().notifications
    
    def get_performance_settings(self) -> PerformanceSettings:
        """Get performance settings."""
        return self.get_all_settings().performance
    
    def update_plus_settings(self, settings_data: Dict[str, Any]) -> bool:
        """
        Update PLUS integration settings.
        
        Args:
            settings_data: New settings data
            
        Returns:
            bool: True if successful
        """
        try:
            current_settings = self.get_all_settings()
            
            # Update PLUS settings
            plus_settings = PlusIntegrationSettings(**settings_data)
            current_settings.plus_integration = plus_settings
            
            # Save and update cache
            success = self.persistence.save_settings(current_settings)
            if success:
                self._update_cache(current_settings)
                logger.info("PLUS integration settings updated successfully")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update PLUS settings: {e}")
            return False
    
    def update_rma_settings(self, settings_data: Dict[str, Any]) -> bool:
        """
        Update RMA processing settings.
        
        Args:
            settings_data: New settings data
            
        Returns:
            bool: True if successful
        """
        try:
            current_settings = self.get_all_settings()
            
            # Update RMA settings
            rma_settings = RmaProcessingSettings(**settings_data)
            current_settings.rma_processing = rma_settings
            
            # Save and update cache
            success = self.persistence.save_settings(current_settings)
            if success:
                self._update_cache(current_settings)
                logger.info("RMA processing settings updated successfully")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update RMA settings: {e}")
            return False
    
    def update_notification_settings(self, settings_data: Dict[str, Any]) -> bool:
        """
        Update notification settings.
        
        Args:
            settings_data: New settings data
            
        Returns:
            bool: True if successful
        """
        try:
            current_settings = self.get_all_settings()
            
            # Update notification settings
            notification_settings = NotificationSettings(**settings_data)
            current_settings.notifications = notification_settings
            
            # Save and update cache
            success = self.persistence.save_settings(current_settings)
            if success:
                self._update_cache(current_settings)
                logger.info("Notification settings updated successfully")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update notification settings: {e}")
            return False
    
    def update_performance_settings(self, settings_data: Dict[str, Any]) -> bool:
        """
        Update performance settings.
        
        Args:
            settings_data: New settings data
            
        Returns:
            bool: True if successful
        """
        try:
            current_settings = self.get_all_settings()
            
            # Update performance settings
            performance_settings = PerformanceSettings(**settings_data)
            current_settings.performance = performance_settings
            
            # Save and update cache
            success = self.persistence.save_settings(current_settings)
            if success:
                self._update_cache(current_settings)
                logger.info("Performance settings updated successfully")
            
            return success
            
        except Exception as e:
            logger.error(f"Failed to update performance settings: {e}")
            return False
    
    async def test_plus_connection(self, connection_data: PlusConnectionTestRequest) -> PlusConnectionTestResponse:
        """
        Test connection to PLUS system.
        
        Args:
            connection_data: Connection parameters
            
        Returns:
            PlusConnectionTestResponse: Test results
        """
        start_time = datetime.now()
        
        try:
            # Convert HttpUrl to string for httpx
            base_url = str(connection_data.base_url)
            
            # Prepare authentication
            auth_data = {
                "username": connection_data.username,
                "password": connection_data.password
            }
            
            if connection_data.api_key:
                auth_data["api_key"] = connection_data.api_key
            
            # Test connection with timeout
            timeout = httpx.Timeout(30.0)
            async with httpx.AsyncClient(timeout=timeout) as client:
                # Try to authenticate or ping the system
                test_endpoints = [
                    f"{base_url}/api/health",
                    f"{base_url}/api/ping",
                    f"{base_url}/health",
                    f"{base_url}/ping",
                    f"{base_url}/"
                ]
                
                last_error = None
                for endpoint in test_endpoints:
                    try:
                        response = await client.get(endpoint)
                        if response.status_code < 500:  # Any non-server error response is good
                            response_time = (datetime.now() - start_time).total_seconds()
                            return PlusConnectionTestResponse(
                                success=True,
                                message="Connection successful",
                                response_time=response_time,
                                server_version=response.headers.get("Server", "Unknown")
                            )
                    except Exception as e:
                        last_error = e
                        continue
                
                # If we get here, all endpoints failed
                raise last_error or Exception("All test endpoints failed")
                
        except asyncio.TimeoutError:
            return PlusConnectionTestResponse(
                success=False,
                message="Connection timeout - server did not respond within 30 seconds"
            )
        except httpx.ConnectError:
            return PlusConnectionTestResponse(
                success=False,
                message="Connection failed - unable to reach server"
            )
        except Exception as e:
            return PlusConnectionTestResponse(
                success=False,
                message=f"Connection test failed: {str(e)}"
            )
    
    def save_plus_credentials(self, credentials: Dict[str, Any]) -> bool:
        """
        Save PLUS system credentials.
        
        Args:
            credentials: Credential data
            
        Returns:
            bool: True if successful
        """
        try:
            # Convert to proper settings format
            settings_data = {
                "base_url": credentials.get("baseUrl", credentials.get("base_url", "")),
                "username": credentials.get("username", ""),
                "password": credentials.get("password", ""),
                "api_key": credentials.get("apiKey", credentials.get("api_key", "")),
            }
            
            # Get current settings and update only credentials
            current_settings = self.get_all_settings()
            plus_settings = current_settings.plus_integration.dict()
            plus_settings.update(settings_data)
            
            return self.update_plus_settings(plus_settings)
            
        except Exception as e:
            logger.error(f"Failed to save PLUS credentials: {e}")
            return False
    
    def export_settings(self, format: str = "yaml") -> Optional[Dict[str, Any]]:
        """
        Export all settings.
        
        Args:
            format: Export format
            
        Returns:
            Dict: Export data
        """
        return self.persistence.export_settings(format)
    
    def import_settings(self, import_data: Dict[str, Any], overwrite: bool = False) -> bool:
        """
        Import settings from data.
        
        Args:
            import_data: Import data
            overwrite: Whether to overwrite existing
            
        Returns:
            bool: True if successful
        """
        success = self.persistence.import_settings(import_data, overwrite)
        if success:
            # Clear cache to force reload
            self._current_settings = None
            self._settings_cache_time = None
        return success
    
    def reset_to_defaults(self) -> bool:
        """
        Reset all settings to defaults.
        
        Returns:
            bool: True if successful
        """
        success = self.persistence.reset_to_defaults()
        if success:
            # Clear cache to force reload
            self._current_settings = None
            self._settings_cache_time = None
            logger.info("Settings reset to defaults")
        return success
    
    def get_system_status(self) -> Dict[str, Any]:
        """
        Get current system status and health metrics.
        
        Returns:
            Dict: System status information
        """
        try:
            import psutil
            import os
            
            # Get system metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # Get process info
            process = psutil.Process(os.getpid())
            process_memory = process.memory_info().rss / 1024 / 1024  # MB
            
            return {
                "cpu_usage": cpu_percent,
                "memory_usage": memory.percent,
                "memory_available": memory.available / 1024 / 1024 / 1024,  # GB
                "disk_usage": disk.percent,
                "disk_free": disk.free / 1024 / 1024 / 1024,  # GB
                "process_memory": process_memory,
                "uptime": (datetime.now() - datetime.fromtimestamp(process.create_time())).total_seconds(),
                "timestamp": datetime.now().isoformat()
            }
            
        except ImportError:
            # If psutil is not available, return basic info
            return {
                "cpu_usage": 0,
                "memory_usage": 0,
                "memory_available": 0,
                "disk_usage": 0,
                "disk_free": 0,
                "process_memory": 0,
                "uptime": 0,
                "timestamp": datetime.now().isoformat(),
                "note": "System metrics not available (psutil not installed)"
            }
        except Exception as e:
            logger.error(f"Failed to get system status: {e}")
            return {
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
