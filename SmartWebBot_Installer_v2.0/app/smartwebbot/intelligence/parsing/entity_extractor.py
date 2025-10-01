"""
Entity Extractor for Intelligent Chat System.

Extracts entities from user commands including URLs, names,
dates, platforms, and other structured information.
"""

import re
from datetime import datetime
from typing import Dict, List, Optional, Any
from ..core.base_chat_component import BaseChatComponent


class EntityExtractor(BaseChatComponent):
    """Extracts structured entities from natural language text."""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        super().__init__("entity_extractor", config)
    
    def initialize(self) -> bool:
        """Initialize the entity extractor."""
        try:
            self.is_initialized = True
            self.is_healthy = True
            return True
        except Exception:
            return False
    
    async def extract(self, text: str) -> Dict[str, Any]:
        """Extract all entities from text."""
        try:
            entities = {}
            
            # Extract URLs
            url_pattern = r'https?://[^\s]+'
            urls = re.findall(url_pattern, text)
            if urls:
                entities['urls'] = urls
                entities['url'] = urls[0]
            
            # Extract emails
            email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
            emails = re.findall(email_pattern, text)
            if emails:
                entities['emails'] = emails
                entities['email'] = emails[0]
            
            # Extract quoted content
            quoted_pattern = r'"([^"]+)"'
            quotes = re.findall(quoted_pattern, text)
            if quotes:
                entities['content'] = quotes[0]
            
            return entities
        except Exception:
            return {}