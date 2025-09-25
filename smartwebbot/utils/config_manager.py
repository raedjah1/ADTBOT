"""
Configuration management system for SmartWebBot.

Handles configuration loading, validation, and environment-specific settings.
"""

import os
import yaml
import json
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, asdict
from ..utils.logger import BotLogger


@dataclass
class BrowserConfig:
    """Browser configuration settings."""
    default_browser: str = "chrome"
    headless: bool = False
    window_size: tuple = (1920, 1080)
    implicit_wait: int = 10
    page_load_timeout: int = 30
    download_directory: str = "downloads"
    user_agent: Optional[str] = None
    proxy: Optional[str] = None
    extensions: list = None
    save_session: bool = True
    
    def __post_init__(self):
        if self.extensions is None:
            self.extensions = []


@dataclass
class AutomationConfig:
    """Automation behavior configuration."""
    screenshot_on_error: bool = True
    retry_attempts: int = 3
    delay_between_actions: float = 1.0
    save_session: bool = True
    element_timeout: int = 10
    smart_wait: bool = True
    anti_detection: bool = True
    human_like_delays: bool = True
    
    
@dataclass
class AIConfig:
    """AI and intelligence configuration."""
    enabled: bool = True
    provider: str = "ollama"  # ollama, openai, groq
    model: str = "gemma3:4b"
    api_key: Optional[str] = None
    ai_endpoint: str = "http://localhost:11434"
    element_detection_model: str = "advanced"
    decision_making_level: str = "adaptive"
    learning_enabled: bool = True
    confidence_threshold: float = 0.8
    fallback_strategies: bool = True
    
    
@dataclass
class SecurityConfig:
    """Security and credential configuration."""
    encryption_enabled: bool = True
    credential_storage: str = "encrypted_file"
    session_encryption: bool = True
    secure_headers: bool = True
    certificate_verification: bool = True
    
    
@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    file_logging: bool = True
    console_logging: bool = True
    json_logging: bool = True
    performance_logging: bool = True
    log_directory: str = "logs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    
    
@dataclass
class DataConfig:
    """Data handling configuration."""
    export_format: str = "csv"
    output_directory: str = "output"
    compression_enabled: bool = True
    data_validation: bool = True
    schema_enforcement: bool = True
    

class ConfigManager:
    """
    Advanced configuration management system.
    
    Features:
    - Multiple configuration sources
    - Environment-specific overrides
    - Configuration validation
    - Hot-reloading
    - Schema enforcement
    """
    
    def __init__(self, config_path: Optional[Union[str, Path]] = None):
        """
        Initialize the configuration manager.
        
        Args:
            config_path: Path to the main configuration file
        """
        self.logger = BotLogger.get_logger("config_manager")
        self.config_path = Path(config_path) if config_path else Path("config.yaml")
        self.config_data: Dict[str, Any] = {}
        self._watchers = []
        
        # Configuration objects
        self.browser: BrowserConfig = BrowserConfig()
        self.automation: AutomationConfig = AutomationConfig()
        self.ai: AIConfig = AIConfig()
        self.security: SecurityConfig = SecurityConfig()
        self.logging: LoggingConfig = LoggingConfig()
        self.data: DataConfig = DataConfig()
        
        self.load_configuration()
    
    def load_configuration(self) -> bool:
        """
        Load configuration from all sources.
        
        Returns:
            bool: True if configuration loaded successfully
        """
        try:
            # Load default configuration
            self._load_defaults()
            
            # Load from configuration file
            if self.config_path.exists():
                self._load_from_file(self.config_path)
            else:
                self.logger.warning(f"Configuration file not found: {self.config_path}")
                self._create_default_config_file()
            
            # Load environment overrides
            self._load_environment_overrides()
            
            # Validate configuration
            if not self._validate_configuration():
                self.logger.error("Configuration validation failed")
                return False
            
            # Update configuration objects
            self._update_config_objects()
            
            self.logger.info("Configuration loaded successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            return False
    
    def _load_defaults(self):
        """Load default configuration values."""
        self.config_data = {
            'browser': asdict(BrowserConfig()),
            'automation': asdict(AutomationConfig()),
            'ai': asdict(AIConfig()),
            'security': asdict(SecurityConfig()),
            'logging': asdict(LoggingConfig()),
            'data': asdict(DataConfig())
        }
    
    def _load_from_file(self, file_path: Path):
        """
        Load configuration from a file.
        
        Args:
            file_path: Path to the configuration file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                if file_path.suffix.lower() in ['.yaml', '.yml']:
                    file_config = yaml.safe_load(file)
                elif file_path.suffix.lower() == '.json':
                    file_config = json.load(file)
                else:
                    raise ValueError(f"Unsupported configuration file format: {file_path.suffix}")
                
                # Deep merge with existing configuration
                self._deep_merge(self.config_data, file_config)
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration file {file_path}: {e}")
            raise
    
    def _load_environment_overrides(self):
        """Load configuration overrides from environment variables."""
        env_prefix = "SMARTWEBBOT_"
        
        for key, value in os.environ.items():
            if key.startswith(env_prefix):
                config_key = key[len(env_prefix):].lower()
                
                # Convert environment variable to nested dict structure
                keys = config_key.split('_')
                current = self.config_data
                
                for key_part in keys[:-1]:
                    if key_part not in current:
                        current[key_part] = {}
                    current = current[key_part]
                
                # Convert value to appropriate type
                final_key = keys[-1]
                current[final_key] = self._convert_env_value(value)
    
    def _convert_env_value(self, value: str) -> Union[str, int, float, bool]:
        """
        Convert environment variable string to appropriate type.
        
        Args:
            value: Environment variable value
        
        Returns:
            Converted value
        """
        # Boolean conversion
        if value.lower() in ['true', 'yes', '1']:
            return True
        elif value.lower() in ['false', 'no', '0']:
            return False
        
        # Number conversion
        try:
            if '.' in value:
                return float(value)
            else:
                return int(value)
        except ValueError:
            pass
        
        # Return as string
        return value
    
    def _deep_merge(self, target: Dict, source: Dict):
        """
        Deep merge two dictionaries.
        
        Args:
            target: Target dictionary to merge into
            source: Source dictionary to merge from
        """
        for key, value in source.items():
            if key in target and isinstance(target[key], dict) and isinstance(value, dict):
                self._deep_merge(target[key], value)
            else:
                target[key] = value
    
    def _validate_configuration(self) -> bool:
        """
        Validate the loaded configuration.
        
        Returns:
            bool: True if configuration is valid
        """
        try:
            # Validate browser configuration
            browser_config = self.config_data.get('browser', {})
            if browser_config.get('default_browser') not in ['chrome', 'firefox', 'edge']:
                self.logger.error("Invalid browser specified")
                return False
            
            # Validate automation configuration
            automation_config = self.config_data.get('automation', {})
            if automation_config.get('retry_attempts', 0) < 0:
                self.logger.error("Retry attempts must be non-negative")
                return False
            
            # Validate AI configuration
            ai_config = self.config_data.get('ai', {})
            confidence_threshold = ai_config.get('confidence_threshold', 0.8)
            if not 0.0 <= confidence_threshold <= 1.0:
                self.logger.error("AI confidence threshold must be between 0.0 and 1.0")
                return False
            
            # Validate logging configuration
            logging_config = self.config_data.get('logging', {})
            if logging_config.get('level') not in ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']:
                self.logger.error("Invalid logging level specified")
                return False
            
            return True
            
        except Exception as e:
            self.logger.error(f"Configuration validation error: {e}")
            return False
    
    def _update_config_objects(self):
        """Update configuration dataclass objects with loaded values."""
        try:
            # Update browser configuration
            browser_data = self.config_data.get('browser', {})
            self.browser = BrowserConfig(**browser_data)
            
            # Update automation configuration
            automation_data = self.config_data.get('automation', {})
            self.automation = AutomationConfig(**automation_data)
            
            # Update AI configuration
            ai_data = self.config_data.get('ai', {})
            self.ai = AIConfig(**ai_data)
            
            # Update security configuration
            security_data = self.config_data.get('security', {})
            self.security = SecurityConfig(**security_data)
            
            # Update logging configuration
            logging_data = self.config_data.get('logging', {})
            self.logging = LoggingConfig(**logging_data)
            
            # Update data configuration
            data_config = self.config_data.get('data', {})
            self.data = DataConfig(**data_config)
            
        except Exception as e:
            self.logger.error(f"Failed to update configuration objects: {e}")
            raise
    
    def _create_default_config_file(self):
        """Create a default configuration file."""
        try:
            default_config = {
                'browser': asdict(BrowserConfig()),
                'automation': asdict(AutomationConfig()),
                'ai': asdict(AIConfig()),
                'security': asdict(SecurityConfig()),
                'logging': asdict(LoggingConfig()),
                'data': asdict(DataConfig())
            }
            
            with open(self.config_path, 'w', encoding='utf-8') as file:
                yaml.dump(default_config, file, default_flow_style=False, indent=2)
            
            self.logger.info(f"Created default configuration file: {self.config_path}")
            
        except Exception as e:
            self.logger.error(f"Failed to create default configuration file: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """
        Get a configuration value by key.
        
        Args:
            key: Configuration key (supports dot notation)
            default: Default value if key not found
        
        Returns:
            Configuration value
        """
        keys = key.split('.')
        current = self.config_data
        
        try:
            for key_part in keys:
                current = current[key_part]
            return current
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> bool:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key (supports dot notation)
            value: Value to set
        
        Returns:
            bool: True if value was set successfully
        """
        keys = key.split('.')
        current = self.config_data
        
        try:
            for key_part in keys[:-1]:
                if key_part not in current:
                    current[key_part] = {}
                current = current[key_part]
            
            current[keys[-1]] = value
            self._update_config_objects()
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to set configuration value {key}: {e}")
            return False
    
    def save_configuration(self, file_path: Optional[Path] = None) -> bool:
        """
        Save current configuration to file.
        
        Args:
            file_path: Path to save configuration to
        
        Returns:
            bool: True if saved successfully
        """
        save_path = file_path or self.config_path
        
        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                yaml.dump(self.config_data, file, default_flow_style=False, indent=2)
            
            self.logger.info(f"Configuration saved to: {save_path}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            return False
    
    def reload_configuration(self) -> bool:
        """
        Reload configuration from all sources.
        
        Returns:
            bool: True if reloaded successfully
        """
        self.logger.info("Reloading configuration")
        return self.load_configuration()
    
    def get_config_summary(self) -> Dict[str, Any]:
        """
        Get a summary of current configuration.
        
        Returns:
            Dict containing configuration summary
        """
        return {
            'browser': asdict(self.browser),
            'automation': asdict(self.automation),
            'ai': asdict(self.ai),
            'security': asdict(self.security),
            'logging': asdict(self.logging),
            'data': asdict(self.data),
            'config_file': str(self.config_path),
            'file_exists': self.config_path.exists()
        }


# Global configuration manager instance
_config_manager: Optional[ConfigManager] = None

def get_config_manager() -> ConfigManager:
    """Get the global configuration manager instance."""
    global _config_manager
    if _config_manager is None:
        _config_manager = ConfigManager()
    return _config_manager

def get_config(key: str, default: Any = None) -> Any:
    """Get a configuration value."""
    return get_config_manager().get(key, default)

def set_config(key: str, value: Any) -> bool:
    """Set a configuration value."""
    return get_config_manager().set(key, value)
