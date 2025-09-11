"""
FastAPI router for settings endpoints.
"""

from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
import logging

from .models import (
    SystemSettings,
    PlusIntegrationSettings,
    RmaProcessingSettings,
    NotificationSettings,
    PerformanceSettings,
    PlusConnectionTestRequest,
    PlusConnectionTestResponse,
    SettingsUpdateResponse,
    SettingsExportResponse
)
from .service import SettingsService

logger = logging.getLogger(__name__)

# Create router
settings_router = APIRouter(prefix="/api", tags=["settings"])

# Dependency to get settings service
def get_settings_service() -> SettingsService:
    """Get settings service instance."""
    return SettingsService()


# PLUS Integration endpoints
@settings_router.post("/plus/test-connection", response_model=PlusConnectionTestResponse)
async def test_plus_connection(
    request: PlusConnectionTestRequest,
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Test connection to PLUS system."""
    try:
        result = await settings_service.test_plus_connection(request)
        return result
    except Exception as e:
        logger.error(f"PLUS connection test failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/plus/save-credentials", response_model=SettingsUpdateResponse)
async def save_plus_credentials(
    credentials: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Save PLUS system credentials."""
    try:
        success = settings_service.save_plus_credentials(credentials)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="PLUS credentials saved successfully",
                updated_fields=list(credentials.keys())
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to save PLUS credentials")
            
    except Exception as e:
        logger.error(f"Failed to save PLUS credentials: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.get("/plus/settings", response_model=PlusIntegrationSettings)
async def get_plus_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get PLUS integration settings."""
    try:
        return settings_service.get_plus_settings()
    except Exception as e:
        logger.error(f"Failed to get PLUS settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.put("/plus/settings", response_model=SettingsUpdateResponse)
async def update_plus_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Update PLUS integration settings."""
    try:
        success = settings_service.update_plus_settings(settings_data)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="PLUS settings updated successfully",
                updated_fields=list(settings_data.keys())
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to update PLUS settings")
            
    except Exception as e:
        logger.error(f"Failed to update PLUS settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# RMA Processing endpoints
@settings_router.get("/rma/settings", response_model=RmaProcessingSettings)
async def get_rma_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get RMA processing settings."""
    try:
        return settings_service.get_rma_settings()
    except Exception as e:
        logger.error(f"Failed to get RMA settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.put("/rma/settings", response_model=SettingsUpdateResponse)
async def update_rma_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Update RMA processing settings."""
    try:
        success = settings_service.update_rma_settings(settings_data)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="RMA settings updated successfully",
                updated_fields=list(settings_data.keys())
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to update RMA settings")
            
    except Exception as e:
        logger.error(f"Failed to update RMA settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/rma/save-settings", response_model=SettingsUpdateResponse)
async def save_rma_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Save RMA processing settings (alias for update)."""
    return await update_rma_settings(settings_data, settings_service)


# Notification endpoints
@settings_router.get("/notifications/settings", response_model=NotificationSettings)
async def get_notification_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get notification settings."""
    try:
        return settings_service.get_notification_settings()
    except Exception as e:
        logger.error(f"Failed to get notification settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.put("/notifications/settings", response_model=SettingsUpdateResponse)
async def update_notification_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Update notification settings."""
    try:
        success = settings_service.update_notification_settings(settings_data)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="Notification settings updated successfully",
                updated_fields=list(settings_data.keys())
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to update notification settings")
            
    except Exception as e:
        logger.error(f"Failed to update notification settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/notifications/save-settings", response_model=SettingsUpdateResponse)
async def save_notification_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Save notification settings (alias for update)."""
    return await update_notification_settings(settings_data, settings_service)


# Performance endpoints
@settings_router.get("/performance/settings", response_model=PerformanceSettings)
async def get_performance_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get performance settings."""
    try:
        return settings_service.get_performance_settings()
    except Exception as e:
        logger.error(f"Failed to get performance settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.put("/performance/settings", response_model=SettingsUpdateResponse)
async def update_performance_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Update performance settings."""
    try:
        success = settings_service.update_performance_settings(settings_data)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="Performance settings updated successfully",
                updated_fields=list(settings_data.keys())
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to update performance settings")
            
    except Exception as e:
        logger.error(f"Failed to update performance settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/performance/save-settings", response_model=SettingsUpdateResponse)
async def save_performance_settings(
    settings_data: Dict[str, Any],
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Save performance settings (alias for update)."""
    return await update_performance_settings(settings_data, settings_service)


# General settings endpoints
@settings_router.get("/settings/all", response_model=SystemSettings)
async def get_all_settings(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get all system settings."""
    try:
        return settings_service.get_all_settings()
    except Exception as e:
        logger.error(f"Failed to get all settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/settings/reset", response_model=SettingsUpdateResponse)
async def reset_settings_to_defaults(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Reset all settings to defaults."""
    try:
        success = settings_service.reset_to_defaults()
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="Settings reset to defaults successfully",
                updated_fields=["all"]
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to reset settings")
            
    except Exception as e:
        logger.error(f"Failed to reset settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.get("/settings/export", response_model=SettingsExportResponse)
async def export_settings(
    format: str = "yaml",
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Export all settings."""
    try:
        export_data = settings_service.export_settings(format)
        
        if export_data:
            return SettingsExportResponse(
                settings=SystemSettings(**export_data["settings"]),
                export_timestamp=export_data["export_timestamp"],
                version=export_data["version"]
            )
        else:
            raise HTTPException(status_code=500, detail="Failed to export settings")
            
    except Exception as e:
        logger.error(f"Failed to export settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@settings_router.post("/settings/import", response_model=SettingsUpdateResponse)
async def import_settings(
    import_data: Dict[str, Any],
    overwrite: bool = False,
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Import settings from data."""
    try:
        success = settings_service.import_settings(import_data, overwrite)
        
        if success:
            return SettingsUpdateResponse(
                success=True,
                message="Settings imported successfully",
                updated_fields=["all"]
            )
        else:
            raise HTTPException(status_code=400, detail="Failed to import settings")
            
    except Exception as e:
        logger.error(f"Failed to import settings: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# System status endpoint
@settings_router.get("/system/status")
async def get_system_status(
    settings_service: SettingsService = Depends(get_settings_service)
):
    """Get current system status and metrics."""
    try:
        return settings_service.get_system_status()
    except Exception as e:
        logger.error(f"Failed to get system status: {e}")
        raise HTTPException(status_code=500, detail=str(e))
