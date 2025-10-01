"""
Base component class for all SmartWebBot modules.

Provides common functionality and interfaces for all components.
"""

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional
from ..utils.logger import BotLogger
from ..utils.config_manager import ConfigManager


class BaseComponent(ABC):
    """
    Abstract base class for all SmartWebBot components.
    
    Provides:
    - Logging capabilities
    - Configuration management
    - Error handling
    - Component lifecycle management
    """
    
    def __init__(self, name: str, config: Optional[Dict] = None):
        """
        Initialize the base component.
        
        Args:
            name: Component name for logging and identification
            config: Component-specific configuration
        """
        self.name = name
        self.config = config or {}
        self.logger = BotLogger.get_logger(self.name)
        self.is_initialized = False
        self.is_active = False
        
        # Component state tracking
        self._state = {}
        self._metrics = {
            'operations_count': 0,
            'success_count': 0,
            'error_count': 0,
            'last_operation_time': None
        }
        
        self.logger.debug(f"Component {self.name} created")
    
    @abstractmethod
    def initialize(self) -> bool:
        """
        Initialize the component.
        
        Returns:
            bool: True if initialization successful
        """
        pass
    
    @abstractmethod
    def cleanup(self) -> bool:
        """
        Clean up component resources.
        
        Returns:
            bool: True if cleanup successful
        """
        pass
    
    def activate(self) -> bool:
        """
        Activate the component for use.
        
        Returns:
            bool: True if activation successful
        """
        if not self.is_initialized:
            if not self.initialize():
                self.logger.error(f"Failed to initialize component {self.name}")
                return False
        
        self.is_active = True
        self.logger.info(f"Component {self.name} activated")
        return True
    
    def deactivate(self) -> bool:
        """
        Deactivate the component.
        
        Returns:
            bool: True if deactivation successful
        """
        self.is_active = False
        success = self.cleanup()
        self.logger.info(f"Component {self.name} deactivated")
        return success
    
    def get_state(self) -> Dict[str, Any]:
        """Get the current component state."""
        return {
            'name': self.name,
            'initialized': self.is_initialized,
            'active': self.is_active,
            'state': self._state.copy(),
            'metrics': self._metrics.copy()
        }
    
    def update_metrics(self, operation: str, success: bool = True):
        """
        Update component metrics.
        
        Args:
            operation: Name of the operation performed
            success: Whether the operation was successful
        """
        import time
        
        self._metrics['operations_count'] += 1
        self._metrics['last_operation_time'] = time.time()
        
        if success:
            self._metrics['success_count'] += 1
        else:
            self._metrics['error_count'] += 1
        
        self.logger.debug(f"Metrics updated for {operation}: success={success}")
    
    def get_success_rate(self) -> float:
        """Get the success rate of operations."""
        if self._metrics['operations_count'] == 0:
            return 0.0
        return self._metrics['success_count'] / self._metrics['operations_count']
    
    def reset_metrics(self):
        """Reset component metrics."""
        self._metrics = {
            'operations_count': 0,
            'success_count': 0,
            'error_count': 0,
            'last_operation_time': None
        }
        self.logger.debug("Component metrics reset")
    
    def validate_config(self, required_keys: list = None) -> bool:
        """
        Validate component configuration.
        
        Args:
            required_keys: List of required configuration keys
        
        Returns:
            bool: True if configuration is valid
        """
        if required_keys:
            missing_keys = [key for key in required_keys if key not in self.config]
            if missing_keys:
                self.logger.error(f"Missing required config keys: {missing_keys}")
                return False
        
        return True
    
    def __enter__(self):
        """Context manager entry."""
        if not self.activate():
            raise RuntimeError(f"Failed to activate component {self.name}")
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.deactivate()
        
        if exc_type is not None:
            self.logger.error(f"Component {self.name} exited with exception: {exc_val}")
            return False
        
        return True
    
    def __repr__(self):
        """String representation of the component."""
        return f"{self.__class__.__name__}(name='{self.name}', active={self.is_active})"
