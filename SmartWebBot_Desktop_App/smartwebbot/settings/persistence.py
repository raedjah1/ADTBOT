"""
Settings persistence layer for file-based storage and retrieval.
"""

import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime
import shutil
import logging

from .models import SystemSettings

logger = logging.getLogger(__name__)


class SettingsPersistence:
    """Handles settings persistence to file system."""
    
    def __init__(self, settings_dir: str = "config", backup_count: int = 5):
        """
        Initialize settings persistence.
        
        Args:
            settings_dir: Directory to store settings files
            backup_count: Number of backup files to keep
        """
        self.settings_dir = Path(settings_dir)
        self.settings_dir.mkdir(exist_ok=True)
        
        self.backup_count = backup_count
        self.settings_file = self.settings_dir / "system_settings.yaml"
        self.backup_dir = self.settings_dir / "backups"
        self.backup_dir.mkdir(exist_ok=True)
        
        # Ensure default settings file exists
        if not self.settings_file.exists():
            self._create_default_settings()
    
    def _create_default_settings(self) -> None:
        """Create default settings file."""
        try:
            default_settings = SystemSettings()
            self.save_settings(default_settings)
            logger.info(f"Created default settings file: {self.settings_file}")
        except Exception as e:
            logger.error(f"Failed to create default settings: {e}")
            raise
    
    def load_settings(self) -> SystemSettings:
        """
        Load settings from file.
        
        Returns:
            SystemSettings: Loaded settings
        """
        try:
            if not self.settings_file.exists():
                logger.warning("Settings file not found, creating default settings")
                self._create_default_settings()
                return SystemSettings()
            
            with open(self.settings_file, 'r', encoding='utf-8') as f:
                data = yaml.safe_load(f)
            
            if not data:
                logger.warning("Empty settings file, using defaults")
                return SystemSettings()
            
            # Clean and validate loaded data
            data = self._clean_loaded_data(data)
            
            settings = SystemSettings(**data)
            logger.debug("Settings loaded successfully")
            return settings
            
        except Exception as e:
            logger.error(f"Failed to load settings: {e}")
            # Create backup of corrupted settings and use defaults
            if self.settings_file.exists():
                try:
                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                    corrupted_file = self.backup_dir / f"corrupted_settings_{timestamp}.yaml"
                    shutil.copy2(self.settings_file, corrupted_file)
                    logger.info(f"Creating backup of corrupted settings and using defaults")
                except Exception:
                    pass
            return SystemSettings()
    
    def _clean_loaded_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and validate loaded settings data.
        
        Args:
            data: Raw loaded data
            
        Returns:
            Dict: Cleaned data
        """
        if not isinstance(data, dict):
            return {}
        
        # Ensure all required sections exist
        default_sections = {
            'plus_integration': {},
            'rma_processing': {},
            'notifications': {},
            'performance': {}
        }
        
        for section, default_values in default_sections.items():
            if section not in data or not isinstance(data[section], dict):
                data[section] = default_values
        
        return data
    
    def _clean_dict_for_yaml(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean dictionary to ensure YAML-safe serialization.
        
        Args:
            data: Dictionary to clean
            
        Returns:
            Dict: Cleaned dictionary
        """
        if isinstance(data, dict):
            cleaned = {}
            for key, value in data.items():
                cleaned[key] = self._clean_dict_for_yaml(value)
            return cleaned
        elif isinstance(data, list):
            return [self._clean_dict_for_yaml(item) for item in data]
        elif hasattr(data, 'value'):  # Enum with value attribute
            return data.value
        elif hasattr(data, '__str__') and hasattr(data, '__class__') and 'Enum' in str(data.__class__):
            return str(data)
        else:
            return data
    
    def save_settings(self, settings: SystemSettings) -> bool:
        """
        Save settings to file with backup.
        
        Args:
            settings: Settings to save
            
        Returns:
            bool: True if successful
        """
        try:
            # Create backup of existing settings
            if self.settings_file.exists():
                self._create_backup()
            
            # Convert to dict and save as YAML
            # Use by_alias=True and exclude_none=False to ensure clean serialization
            settings_dict = settings.dict(by_alias=True, exclude_none=False)
            
            # Clean any enum values to ensure they're serialized as strings
            settings_dict = self._clean_dict_for_yaml(settings_dict)
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                # Use safe_dump to prevent Python object serialization
                yaml.safe_dump(
                    settings_dict, 
                    f, 
                    default_flow_style=False, 
                    indent=2,
                    allow_unicode=True,
                    sort_keys=False
                )
            
            logger.info("Settings saved successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to save settings: {e}")
            return False
    
    def _create_backup(self) -> None:
        """Create backup of current settings file."""
        try:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"settings_backup_{timestamp}.yaml"
            
            shutil.copy2(self.settings_file, backup_file)
            logger.debug(f"Created settings backup: {backup_file}")
            
            # Clean old backups
            self._cleanup_old_backups()
            
        except Exception as e:
            logger.warning(f"Failed to create settings backup: {e}")
    
    def _cleanup_old_backups(self) -> None:
        """Remove old backup files, keeping only the most recent ones."""
        try:
            backup_files = sorted(
                self.backup_dir.glob("settings_backup_*.yaml"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            )
            
            # Remove excess backups
            for backup_file in backup_files[self.backup_count:]:
                backup_file.unlink()
                logger.debug(f"Removed old backup: {backup_file}")
                
        except Exception as e:
            logger.warning(f"Failed to cleanup old backups: {e}")
    
    def export_settings(self, format: str = "yaml") -> Optional[Dict[str, Any]]:
        """
        Export settings in specified format.
        
        Args:
            format: Export format ('yaml' or 'json')
            
        Returns:
            Dict containing export data
        """
        try:
            settings = self.load_settings()
            export_data = {
                "settings": settings.dict(),
                "export_timestamp": datetime.now().isoformat(),
                "version": "1.0",
                "format": format
            }
            
            return export_data
            
        except Exception as e:
            logger.error(f"Failed to export settings: {e}")
            return None
    
    def import_settings(self, import_data: Dict[str, Any], overwrite: bool = False) -> bool:
        """
        Import settings from export data.
        
        Args:
            import_data: Previously exported settings data
            overwrite: Whether to overwrite existing settings
            
        Returns:
            bool: True if successful
        """
        try:
            if not overwrite and self.settings_file.exists():
                logger.warning("Settings file exists and overwrite=False")
                return False
            
            settings_data = import_data.get("settings", {})
            settings = SystemSettings(**settings_data)
            
            return self.save_settings(settings)
            
        except Exception as e:
            logger.error(f"Failed to import settings: {e}")
            return False
    
    def reset_to_defaults(self) -> bool:
        """
        Reset settings to default values.
        
        Returns:
            bool: True if successful
        """
        try:
            # Create backup first
            if self.settings_file.exists():
                self._create_backup()
            
            # Create and save default settings
            default_settings = SystemSettings()
            return self.save_settings(default_settings)
            
        except Exception as e:
            logger.error(f"Failed to reset settings to defaults: {e}")
            return False
    
    def get_backups_list(self) -> list[Dict[str, Any]]:
        """
        Get list of available backup files.
        
        Returns:
            List of backup file information
        """
        try:
            backups = []
            for backup_file in sorted(
                self.backup_dir.glob("settings_backup_*.yaml"),
                key=lambda x: x.stat().st_mtime,
                reverse=True
            ):
                stat = backup_file.stat()
                backups.append({
                    "filename": backup_file.name,
                    "created": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                    "size": stat.st_size
                })
            
            return backups
            
        except Exception as e:
            logger.error(f"Failed to get backups list: {e}")
            return []
    
    def restore_from_backup(self, backup_filename: str) -> bool:
        """
        Restore settings from a backup file.
        
        Args:
            backup_filename: Name of backup file to restore from
            
        Returns:
            bool: True if successful
        """
        try:
            backup_file = self.backup_dir / backup_filename
            if not backup_file.exists():
                logger.error(f"Backup file not found: {backup_filename}")
                return False
            
            # Create backup of current settings before restoring
            if self.settings_file.exists():
                self._create_backup()
            
            # Copy backup to main settings file
            shutil.copy2(backup_file, self.settings_file)
            logger.info(f"Settings restored from backup: {backup_filename}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to restore from backup: {e}")
            return False
