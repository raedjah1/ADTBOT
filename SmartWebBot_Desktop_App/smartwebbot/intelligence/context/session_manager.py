"""
Smart Session Manager for Intelligent Chat System.

Manages chat sessions, context, and state with comprehensive
lifecycle management and data persistence.
"""

import time
import uuid
from datetime import datetime
from typing import Dict, Optional, Any, List
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import ISessionManager, ISessionContext


class SmartSessionManager(BaseChatComponent, ISessionManager):
    """
    Smart session manager with comprehensive session lifecycle management.
    
    Features:
    - Session creation and lifecycle management
    - Context persistence and retrieval
    - Session cleanup and garbage collection
    - Performance monitoring
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("smart_session_manager", config)
        
        # Session storage
        self.sessions: Dict[str, ISessionContext] = {}
        
        # Configuration
        self.session_timeout = self.get_config_value("session_timeout", 3600)  # 1 hour
        self.max_sessions = self.get_config_value("max_sessions", 1000)
        self.cleanup_interval = self.get_config_value("cleanup_interval", 300)  # 5 minutes
        
        # Metrics
        self.session_metrics = {
            "total_created": 0,
            "active_sessions": 0,
            "expired_sessions": 0
        }
    
    def initialize(self) -> bool:
        """Initialize the session manager."""
        try:
            self.logger.info("Initializing Smart Session Manager...")
            
            self.is_initialized = True
            self.is_healthy = True
            
            self.logger.info("Smart Session Manager initialized successfully")
            return True
            
        except Exception as e:
            self.log_error(e, "Session manager initialization")
            return False
    
    async def create_session(self, user_id: Optional[str] = None) -> str:
        """Create new chat session."""
        
        # Check session limit
        if len(self.sessions) >= self.max_sessions:
            await self._cleanup_expired_sessions()
            
            if len(self.sessions) >= self.max_sessions:
                raise Exception(f"Maximum sessions ({self.max_sessions}) reached")
        
        # Generate session ID
        session_id = str(uuid.uuid4())
        
        # Create session context
        session_context = ISessionContext(
            session_id=session_id,
            user_id=user_id,
            current_url=None,
            credentials={},
            workflow_state={},
            execution_history=[],
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
        
        # Store session
        self.sessions[session_id] = session_context
        
        # Update metrics
        self.session_metrics["total_created"] += 1
        self.session_metrics["active_sessions"] = len(self.sessions)
        
        self.logger.info(f"Created session: {session_id}")
        self.increment_metric("sessions_created")
        
        return session_id
    
    async def get_session(self, session_id: str) -> Optional[ISessionContext]:
        """Get session context by ID."""
        
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        
        # Check if session is expired
        if self._is_session_expired(session):
            await self.end_session(session_id)
            return None
        
        # Update last activity
        session.last_activity = datetime.utcnow()
        
        return session
    
    async def update_session(self, session_id: str, updates: Dict[str, Any]) -> bool:
        """Update session context."""
        
        if session_id not in self.sessions:
            self.logger.warning(f"Session not found for update: {session_id}")
            return False
        
        try:
            session = self.sessions[session_id]
            
            # Update allowed fields
            if "current_url" in updates:
                session.current_url = updates["current_url"]
            
            if "workflow_state" in updates:
                session.workflow_state.update(updates["workflow_state"])
            
            if "user_id" in updates:
                session.user_id = updates["user_id"]
            
            # Update last activity
            session.last_activity = datetime.utcnow()
            
            self.logger.debug(f"Updated session: {session_id}")
            return True
            
        except Exception as e:
            self.log_error(e, f"Session update failed: {session_id}")
            return False
    
    async def end_session(self, session_id: str) -> bool:
        """End chat session."""
        
        if session_id not in self.sessions:
            return False
        
        try:
            # Remove session
            del self.sessions[session_id]
            
            # Update metrics
            self.session_metrics["active_sessions"] = len(self.sessions)
            
            self.logger.info(f"Ended session: {session_id}")
            self.increment_metric("sessions_ended")
            
            return True
            
        except Exception as e:
            self.log_error(e, f"Session end failed: {session_id}")
            return False
    
    def _is_session_expired(self, session: ISessionContext) -> bool:
        """Check if session is expired."""
        
        current_time = datetime.utcnow()
        time_since_activity = (current_time - session.last_activity).total_seconds()
        
        return time_since_activity > self.session_timeout
    
    async def _cleanup_expired_sessions(self) -> int:
        """Clean up expired sessions."""
        
        expired_sessions = []
        current_time = datetime.utcnow()
        
        for session_id, session in self.sessions.items():
            if self._is_session_expired(session):
                expired_sessions.append(session_id)
        
        # Remove expired sessions
        for session_id in expired_sessions:
            await self.end_session(session_id)
        
        if expired_sessions:
            self.logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")
            self.session_metrics["expired_sessions"] += len(expired_sessions)
        
        return len(expired_sessions)
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get information about all active sessions."""
        
        active_sessions = []
        current_time = datetime.utcnow()
        
        for session_id, session in self.sessions.items():
            if not self._is_session_expired(session):
                session_info = {
                    "session_id": session_id,
                    "user_id": session.user_id,
                    "created_at": session.created_at.isoformat(),
                    "last_activity": session.last_activity.isoformat(),
                    "current_url": session.current_url,
                    "has_credentials": bool(session.credentials),
                    "execution_history_count": len(session.execution_history),
                    "age_seconds": (current_time - session.created_at).total_seconds()
                }
                active_sessions.append(session_info)
        
        return active_sessions
    
    def get_session_metrics(self) -> Dict[str, Any]:
        """Get session management metrics."""
        
        return {
            **self.session_metrics,
            "current_active": len(self.sessions),
            "average_session_age": self._calculate_average_session_age(),
            "memory_usage_mb": self._estimate_memory_usage()
        }
    
    def _calculate_average_session_age(self) -> float:
        """Calculate average age of active sessions."""
        
        if not self.sessions:
            return 0.0
        
        current_time = datetime.utcnow()
        total_age = 0
        
        for session in self.sessions.values():
            age = (current_time - session.created_at).total_seconds()
            total_age += age
        
        return total_age / len(self.sessions)
    
    def _estimate_memory_usage(self) -> float:
        """Estimate memory usage of sessions (rough estimate)."""
        
        # Rough estimate: 1KB per session + 100 bytes per execution history entry
        base_size = len(self.sessions) * 1024  # 1KB per session
        
        history_size = 0
        for session in self.sessions.values():
            history_size += len(session.execution_history) * 100  # 100 bytes per entry
        
        total_bytes = base_size + history_size
        return total_bytes / (1024 * 1024)  # Convert to MB
