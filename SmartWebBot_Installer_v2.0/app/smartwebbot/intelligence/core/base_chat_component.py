"""
Base class for all intelligent chat components.

Provides common functionality like logging, configuration,
health monitoring, and lifecycle management.
"""

import logging
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod


class BaseChatComponent(ABC):
    """
    Base class for all intelligent chat components.
    
    Provides:
    - Standardized logging
    - Configuration management
    - Health monitoring
    - Lifecycle management
    - Metrics collection
    """
    
    def __init__(self, component_name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize base chat component."""
        self.component_name = component_name
        self.config = config or {}
        self.logger = logging.getLogger(f"smartwebbot.intelligence.{component_name}")
        
        # Component state
        self.is_initialized = False
        self.is_healthy = True
        self.metrics = {
            "requests_processed": 0,
            "errors_encountered": 0,
            "average_response_time": 0.0
        }
    
    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the component. Must be implemented by subclasses."""
        pass
    
    def cleanup(self) -> bool:
        """Clean up component resources. Override if needed."""
        try:
            self.logger.info(f"Cleaning up {self.component_name}")
            self.is_initialized = False
            return True
        except Exception as e:
            self.logger.error(f"Cleanup failed for {self.component_name}: {e}")
            return False
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get component health status."""
        return {
            "component": self.component_name,
            "is_initialized": self.is_initialized,
            "is_healthy": self.is_healthy,
            "metrics": self.metrics.copy()
        }
    
    def update_metrics(self, metric_name: str, value: Any) -> None:
        """Update component metrics."""
        self.metrics[metric_name] = value
    
    def increment_metric(self, metric_name: str, increment: int = 1) -> None:
        """Increment a metric counter."""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = 0
        self.metrics[metric_name] += increment
    
    def log_error(self, error: Exception, context: Optional[str] = None) -> None:
        """Log error and update error metrics."""
        error_msg = f"{context}: {error}" if context else str(error)
        self.logger.error(error_msg, exc_info=True)
        self.increment_metric("errors_encountered")
        self.is_healthy = False
    
    def log_success(self, message: str, response_time: float = 0.0) -> None:
        """Log successful operation and update metrics."""
        self.logger.debug(f"{self.component_name} success: {message}")
        self.increment_metric("requests_processed")
        
        # Update average response time
        if response_time > 0:
            current_avg = self.metrics.get("average_response_time", 0.0)
            processed = self.metrics.get("requests_processed", 1)
            new_avg = ((current_avg * (processed - 1)) + response_time) / processed
            self.update_metrics("average_response_time", round(new_avg, 3))
    
    def get_config_value(self, key: str, default: Any = None) -> Any:
        """Get configuration value with fallback."""
        return self.config.get(key, default)
    
    def validate_config(self, required_keys: list) -> bool:
        """Validate that required configuration keys are present."""
        missing_keys = [key for key in required_keys if key not in self.config]
        if missing_keys:
            self.logger.error(f"Missing required config keys: {missing_keys}")
            return False
        return True
