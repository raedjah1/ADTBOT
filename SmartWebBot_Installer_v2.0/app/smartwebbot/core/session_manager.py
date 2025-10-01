"""
Session management for SmartWebBot.

Handles session persistence, restoration, and management.
"""

import json
import time
from pathlib import Path
from typing import Dict, Optional, Any
from ..core.base_component import BaseComponent


class SessionManager(BaseComponent):
    """
    Session management system for SmartWebBot.
    """
    
    def __init__(self, config: Dict = None):
        """Initialize the session manager."""
        super().__init__("session_manager", config)
        self.sessions_dir = Path("sessions")
        
    def initialize(self) -> bool:
        """Initialize the session manager."""
        try:
            self.sessions_dir.mkdir(exist_ok=True)
            self.is_initialized = True
            return True
        except Exception as e:
            self.logger.error(f"Session manager initialization failed: {e}")
            return False
    
    def cleanup(self) -> bool:
        """Clean up session manager."""
        return True
    
    def save_session(self, session_data: Dict[str, Any]) -> str:
        """Save a session to file."""
        try:
            session_id = f"session_{int(time.time())}"
            session_file = self.sessions_dir / f"{session_id}.json"
            
            with open(session_file, 'w') as f:
                json.dump(session_data, f, indent=2, default=str)
            
            self.logger.info(f"Session saved: {session_file}")
            return session_id
            
        except Exception as e:
            self.logger.error(f"Failed to save session: {e}")
            return ""
    
    def load_session(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Load a session from file."""
        try:
            session_file = self.sessions_dir / f"{session_id}.json"
            
            if not session_file.exists():
                self.logger.warning(f"Session file not found: {session_file}")
                return None
            
            with open(session_file, 'r') as f:
                session_data = json.load(f)
            
            self.logger.info(f"Session loaded: {session_file}")
            return session_data
            
        except Exception as e:
            self.logger.error(f"Failed to load session: {e}")
            return None
