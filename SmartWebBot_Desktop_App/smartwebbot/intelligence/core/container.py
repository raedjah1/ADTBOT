"""
Dependency Injection Container for Intelligent Chat System.

Manages component lifecycle and dependencies with perfect
separation of concerns and loose coupling.
"""

from typing import Dict, Type, Any, Callable, TypeVar, Optional
import inspect
from abc import ABC

T = TypeVar('T')


class ComponentContainer:
    """
    Simple component container for the modular system.
    
    This is a simplified version focused on instance management.
    """
    
    def __init__(self):
        self.instances = {}
        self.configs = {}
        self.is_initialized = False
    
    def initialize(self) -> bool:
        """Initialize the container."""
        self.is_initialized = True
        return True
    
    def register_instance(self, name: str, instance) -> None:
        """Register a component instance."""
        self.instances[name] = instance
    
    def get_instance(self, name: str):
        """Get a component instance."""
        return self.instances.get(name)
    
    def register_config(self, name: str, config: dict) -> None:
        """Register configuration for a component."""
        self.configs[name] = config
    
    def get_config(self, name: str) -> dict:
        """Get configuration for a component."""
        return self.configs.get(name, {})
    
    def get_status(self) -> dict:
        """Get container status."""
        return {
            "initialized": self.is_initialized,
            "registered_instances": list(self.instances.keys()),
            "registered_configs": list(self.configs.keys())
        }
    
    def cleanup(self) -> None:
        """Clean up container resources."""
        for instance in self.instances.values():
            if hasattr(instance, 'cleanup'):
                try:
                    instance.cleanup()
                except Exception:
                    pass
        
        self.instances.clear()
        self.configs.clear()


class ServiceBuilder:
    """Builder for configuring services in component container."""
    
    def __init__(self, container: ComponentContainer):
        self.container = container
    
    def add_instance(self, name: str, instance) -> 'ServiceBuilder':
        """Add existing instance."""
        self.container.register_instance(name, instance)
        return self
    
    def build(self) -> ComponentContainer:
        """Build configured container."""
        return self.container


def create_chat_container() -> ComponentContainer:
    """Create and configure container for intelligent chat system."""
    return ComponentContainer()