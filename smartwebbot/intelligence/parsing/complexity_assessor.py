"""
Complexity Assessor for Intelligent Chat System.

Assesses the complexity of user commands to determine
execution strategy and resource requirements.
"""

from typing import Dict, Optional, Any
from ..core.base_chat_component import BaseChatComponent
from ..core.interfaces import CommandComplexity


class ComplexityAssessor(BaseChatComponent):
    """Assesses command complexity for optimal execution planning."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("complexity_assessor", config)
    
    def initialize(self) -> bool:
        """Initialize the complexity assessor."""
        try:
            self.is_initialized = True
            self.is_healthy = True
            return True
        except Exception:
            return False
    
    async def assess(self, text: str, intent: str, parameters: Dict[str, Any]) -> CommandComplexity:
        """Assess command complexity."""
        try:
            word_count = len(text.split())
            
            if intent in ["marketing_campaign"]:
                return CommandComplexity.ADVANCED
            elif intent in ["social_media_post", "data_extraction"]:
                return CommandComplexity.COMPLEX
            elif intent in ["login_to_platform", "form_interaction"]:
                return CommandComplexity.MODERATE
            elif word_count > 20:
                return CommandComplexity.COMPLEX
            elif word_count > 10:
                return CommandComplexity.MODERATE
            else:
                return CommandComplexity.SIMPLE
        except Exception:
            return CommandComplexity.SIMPLE