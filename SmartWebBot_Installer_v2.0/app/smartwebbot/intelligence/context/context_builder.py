"""
Context Builder for Intelligent Chat System.

Builds and enriches execution context for workflow operations
with comprehensive session and environmental data.
"""

from typing import Dict, Optional, Any
from datetime import datetime
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import IContextBuilder, ISessionContext, IParsedCommand


class ContextBuilder(BaseChatComponent, IContextBuilder):
    """Builds execution context for workflow operations."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("context_builder", config)
    
    def initialize(self) -> bool:
        """Initialize the context builder."""
        try:
            self.is_initialized = True
            self.is_healthy = True
            return True
        except Exception:
            return False
    
    async def build_context(self, session_id: str, command: IParsedCommand) -> ISessionContext:
        """Build execution context for command."""
        return ISessionContext(
            session_id=session_id,
            user_id=None,
            current_url=command.parameters.get('url'),
            credentials={},
            workflow_state={},
            execution_history=[],
            created_at=datetime.utcnow(),
            last_activity=datetime.utcnow()
        )
    
    async def enrich_context(self, context: ISessionContext, additional_data: Dict[str, Any]) -> ISessionContext:
        """Enrich context with additional data."""
        context.workflow_state.update(additional_data)
        context.last_activity = datetime.utcnow()
        return context
