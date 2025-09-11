"""
SmartWebBot - Advanced Intelligent Web Automation Framework

A state-of-the-art web automation framework with AI-powered intelligence,
modular architecture, and enterprise-grade features.

Author: SmartWebBot Team
Version: 2.0.0
License: MIT
"""

from .core.bot_engine import SmartWebBot, smart_bot
from .core.session_manager import SessionManager
from .intelligence.ai_detector import AIElementDetector
from .intelligence.decision_engine import DecisionEngine
from .automation.web_controller import WebController
from .automation.form_handler import FormHandler
from .automation.navigation_manager import NavigationManager
from .data.extractor import DataExtractor
from .data.exporter import DataExporter
from .security.credential_manager import CredentialManager
from .utils.logger import BotLogger
from .utils.config_manager import ConfigManager

__version__ = "2.0.0"
__author__ = "SmartWebBot Team"
__license__ = "MIT"

# Main exports
__all__ = [
    "SmartWebBot",
    "smart_bot",
    "SessionManager", 
    "AIElementDetector",
    "DecisionEngine",
    "WebController",
    "FormHandler",
    "NavigationManager",
    "DataExtractor",
    "DataExporter",
    "CredentialManager",
    "BotLogger",
    "ConfigManager"
]

# Version info
VERSION_INFO = {
    "major": 2,
    "minor": 0,
    "patch": 0,
    "release": "stable"
}

def get_version():
    """Get the current version string."""
    return __version__

def get_version_info():
    """Get detailed version information."""
    return VERSION_INFO.copy()
