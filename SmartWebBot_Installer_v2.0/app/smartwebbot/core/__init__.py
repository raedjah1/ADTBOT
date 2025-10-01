"""
Core module for SmartWebBot

Contains the main bot engine and core functionality.
"""

from .bot_engine import SmartWebBot
from .session_manager import SessionManager
from .base_component import BaseComponent

__all__ = ["SmartWebBot", "SessionManager", "BaseComponent"]
