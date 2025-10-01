"""
Automation module for SmartWebBot

Contains specialized automation components for different types of web interactions.
"""

from .web_controller import WebController
from .form_handler import FormHandler
from .navigation_manager import NavigationManager
from .interaction_manager import InteractionManager

__all__ = ["WebController", "FormHandler", "NavigationManager", "InteractionManager"]
