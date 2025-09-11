"""
Advanced logging system for SmartWebBot.

Provides structured logging with multiple handlers, formatters,
and integration with monitoring systems.
"""

import os
import logging
import logging.handlers
import json
from datetime import datetime
from typing import Dict, Optional, Any
from pathlib import Path


class BotLogger:
    """
    Advanced logging system for SmartWebBot components.
    
    Features:
    - Multiple log levels and handlers
    - Structured JSON logging
    - Rotation and archival
    - Performance metrics
    - Error tracking
    """
    
    _loggers: Dict[str, logging.Logger] = {}
    _initialized = False
    _config = {}
    
    @classmethod
    def initialize(cls, config: Dict[str, Any] = None):
        """
        Initialize the logging system.
        
        Args:
            config: Logging configuration
        """
        if cls._initialized:
            return
        
        cls._config = config or {
            'level': 'INFO',
            'format': 'detailed',
            'file_logging': True,
            'console_logging': True,
            'json_logging': True,
            'log_directory': 'logs',
            'max_file_size': 10 * 1024 * 1024,  # 10MB
            'backup_count': 5,
            'performance_logging': True
        }
        
        # Create log directory
        log_dir = Path(cls._config['log_directory'])
        log_dir.mkdir(exist_ok=True)
        
        cls._initialized = True
    
    @classmethod
    def get_logger(cls, name: str) -> logging.Logger:
        """
        Get or create a logger for a component.
        
        Args:
            name: Logger name (usually component name)
        
        Returns:
            logging.Logger: Configured logger instance
        """
        if not cls._initialized:
            cls.initialize()
        
        if name in cls._loggers:
            return cls._loggers[name]
        
        logger = logging.getLogger(f"smartwebbot.{name}")
        logger.setLevel(getattr(logging, cls._config['level']))
        
        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()
        
        # Console handler
        if cls._config.get('console_logging', True):
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            
            if cls._config.get('format') == 'simple':
                console_format = logging.Formatter(
                    '%(levelname)s - %(name)s - %(message)s'
                )
            else:
                console_format = logging.Formatter(
                    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S'
                )
            
            console_handler.setFormatter(console_format)
            logger.addHandler(console_handler)
        
        # File handler with rotation
        if cls._config.get('file_logging', True):
            log_file = Path(cls._config['log_directory']) / f"{name}.log"
            file_handler = logging.handlers.RotatingFileHandler(
                log_file,
                maxBytes=cls._config.get('max_file_size', 10 * 1024 * 1024),
                backupCount=cls._config.get('backup_count', 5)
            )
            file_handler.setLevel(logging.DEBUG)
            
            file_format = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            file_handler.setFormatter(file_format)
            logger.addHandler(file_handler)
        
        # JSON handler for structured logging
        if cls._config.get('json_logging', True):
            json_log_file = Path(cls._config['log_directory']) / f"{name}.json"
            json_handler = logging.handlers.RotatingFileHandler(
                json_log_file,
                maxBytes=cls._config.get('max_file_size', 10 * 1024 * 1024),
                backupCount=cls._config.get('backup_count', 5)
            )
            json_handler.setLevel(logging.DEBUG)
            json_handler.setFormatter(JSONFormatter())
            logger.addHandler(json_handler)
        
        # Performance handler
        if cls._config.get('performance_logging', True):
            perf_log_file = Path(cls._config['log_directory']) / f"{name}_performance.log"
            perf_handler = logging.handlers.RotatingFileHandler(
                perf_log_file,
                maxBytes=cls._config.get('max_file_size', 10 * 1024 * 1024),
                backupCount=cls._config.get('backup_count', 5)
            )
            perf_handler.setLevel(logging.INFO)
            perf_handler.addFilter(PerformanceFilter())
            perf_handler.setFormatter(JSONFormatter())
            logger.addHandler(perf_handler)
        
        cls._loggers[name] = logger
        return logger
    
    @classmethod
    def log_performance(cls, logger_name: str, operation: str, 
                       duration: float, success: bool = True, **kwargs):
        """
        Log performance metrics.
        
        Args:
            logger_name: Name of the logger
            operation: Operation name
            duration: Operation duration in seconds
            success: Whether operation was successful
            **kwargs: Additional metrics
        """
        logger = cls.get_logger(logger_name)
        
        perf_data = {
            'type': 'performance',
            'operation': operation,
            'duration': duration,
            'success': success,
            'timestamp': datetime.now().isoformat(),
            **kwargs
        }
        
        logger.info(f"PERFORMANCE: {json.dumps(perf_data)}")
    
    @classmethod
    def log_error(cls, logger_name: str, error: Exception, 
                  context: Dict[str, Any] = None):
        """
        Log error with context information.
        
        Args:
            logger_name: Name of the logger
            error: Exception that occurred
            context: Additional context information
        """
        logger = cls.get_logger(logger_name)
        
        error_data = {
            'type': 'error',
            'error_type': type(error).__name__,
            'error_message': str(error),
            'timestamp': datetime.now().isoformat(),
            'context': context or {}
        }
        
        logger.error(f"ERROR: {json.dumps(error_data)}", exc_info=True)
    
    @classmethod
    def set_level(cls, level: str):
        """
        Set logging level for all loggers.
        
        Args:
            level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        """
        log_level = getattr(logging, level.upper())
        
        for logger in cls._loggers.values():
            logger.setLevel(log_level)
        
        cls._config['level'] = level.upper()


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record):
        """Format log record as JSON."""
        log_data = {
            'timestamp': datetime.fromtimestamp(record.created).isoformat(),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        if record.exc_info:
            log_data['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_data)


class PerformanceFilter(logging.Filter):
    """Filter to only allow performance-related log records."""
    
    def filter(self, record):
        """Filter performance log records."""
        return hasattr(record, 'msg') and 'PERFORMANCE:' in str(record.msg)


# Convenience functions
def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return BotLogger.get_logger(name)

def log_performance(logger_name: str, operation: str, duration: float, **kwargs):
    """Log performance metrics."""
    BotLogger.log_performance(logger_name, operation, duration, **kwargs)

def log_error(logger_name: str, error: Exception, context: Dict = None):
    """Log error with context."""
    BotLogger.log_error(logger_name, error, context)
