"""
AI Service Module

Business logic for AI operations with proper separation of concerns.
"""

import asyncio
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime

from ..intelligence.chat_ai import ChatAI
from ..intelligence.ai_detector import AIElementDetector
from ..intelligence.ai_vulnerability_scanner import AIVulnerabilityScanner
from ..intelligence.ai_social_engineer import AISocialEngineer
from ..intelligence.ai_adaptive_evasion import AIAdaptiveEvasion
from ..intelligence.ai_reconnaissance import AIReconnaissance
from ..utils.config_manager import get_config_manager
from ..utils.logger import BotLogger

class AIService:
    """
    Service layer for AI operations.
    
    Handles business logic, error handling, and coordination between AI modules.
    """
    
    def __init__(self):
        self.logger = BotLogger().get_logger("ai_service")
        self.config_manager = get_config_manager()
        
        # AI modules
        self._chat_ai: Optional[ChatAI] = None
        self._element_detector: Optional[AIElementDetector] = None
        self._vuln_scanner: Optional[AIVulnerabilityScanner] = None
        self._social_engineer: Optional[AISocialEngineer] = None
        self._adaptive_evasion: Optional[AIAdaptiveEvasion] = None
        self._reconnaissance: Optional[AIReconnaissance] = None
        
        # Configuration
        self._config = self._load_config()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load AI configuration from config manager."""
        return {
            "provider": self.config_manager.get("ai.provider", "ollama"),
            "model": self.config_manager.get("ai.model", "gemma3:4b"),
            "api_key": self.config_manager.get("ai.api_key"),
            "ai_endpoint": self.config_manager.get("ai.ai_endpoint", "http://localhost:11434"),
            "confidence_threshold": self.config_manager.get("ai.confidence_threshold", 0.8),
            "learning_enabled": self.config_manager.get("ai.learning_enabled", True)
        }
    
    async def initialize(self) -> bool:
        """Initialize all AI modules."""
        try:
            # Initialize Chat AI
            self._chat_ai = ChatAI(self._config)
            if not self._chat_ai.initialize():
                self.logger.error("Failed to initialize Chat AI")
                return False
            
            # Initialize other AI modules
            self._element_detector = AIElementDetector(self._config)
            self._vuln_scanner = AIVulnerabilityScanner(self._config)
            self._social_engineer = AISocialEngineer(self._config)
            self._adaptive_evasion = AIAdaptiveEvasion(self._config)
            self._reconnaissance = AIReconnaissance(self._config)
            
            # Initialize all modules
            modules = [
                self._element_detector,
                self._vuln_scanner,
                self._social_engineer,
                self._adaptive_evasion,
                self._reconnaissance
            ]
            
            for module in modules:
                if module and not module.initialize():
                    self.logger.warning(f"Failed to initialize {module.__class__.__name__}")
            
            self.logger.info("AI Service initialized successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to initialize AI Service: {e}")
            return False
    
    async def chat(self, message: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """Handle chat with AI."""
        if not self._chat_ai:
            raise Exception("AI Service not initialized")
        
        try:
            response = await self._chat_ai.chat(message)
            response["session_id"] = session_id or f"session_{int(datetime.now().timestamp())}"
            response["timestamp"] = datetime.now().isoformat()
            return response
        except Exception as e:
            self.logger.error(f"Chat failed: {e}")
            raise
    
    async def generate_task_suggestion(self, description: str) -> Dict[str, Any]:
        """Generate task suggestions based on description."""
        if not self._chat_ai:
            raise Exception("AI Service not initialized")
        
        try:
            prompt = f"""
            Create a web automation task for: "{description}"
            
            Return JSON with:
            - name: Clear task name
            - description: What it does
            - actions: Array of automation steps
            - confidence: 0.0-1.0
            
            Available actions: navigate_to, fill_form, click_element, extract_data, 
            take_screenshot, wait, scroll, create_jira_ticket, update_jira_status, extract_jira_issues
            """
            
            response = await self._chat_ai.chat(prompt)
            
            # Try to extract JSON from response
            try:
                import re
                json_match = re.search(r'\{.*\}', response.get("response", ""), re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            
            # Fallback response
            return {
                "name": f"AI Task: {description[:50]}...",
                "description": description,
                "actions": [
                    {"type": "navigate_to", "url": "https://example.com"},
                    {"type": "take_screenshot", "filename": "task_screenshot"}
                ],
                "confidence": 0.5
            }
            
        except Exception as e:
            self.logger.error(f"Task suggestion failed: {e}")
            raise
    
    async def analyze_website(self, url: str, analysis_type: str = "general") -> Dict[str, Any]:
        """Analyze website using AI."""
        if not self._chat_ai:
            raise Exception("AI Service not initialized")
        
        try:
            prompt = f"""
            Analyze website: {url}
            Type: {analysis_type}
            
            Provide:
            1. Automation opportunities
            2. Form fields and elements
            3. Security considerations
            4. Recommended approach
            5. Potential challenges
            
            Be specific and actionable.
            """
            
            response = await self._chat_ai.chat(prompt)
            
            return {
                "url": url,
                "analysis_type": analysis_type,
                "analysis": response.get("response", ""),
                "suggestions": response.get("actions", []),
                "confidence": response.get("confidence", 0.0),
                "timestamp": datetime.now().isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Website analysis failed: {e}")
            raise
    
    async def detect_elements(self, page_source: str, target_elements: List[str]) -> Dict[str, Any]:
        """Detect elements on a page using AI."""
        if not self._element_detector:
            raise Exception("Element Detector not initialized")
        
        try:
            # This would use the AI element detector
            # For now, return a placeholder
            return {
                "elements_found": len(target_elements),
                "detected_elements": target_elements,
                "confidence": 0.8,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Element detection failed: {e}")
            raise
    
    async def scan_vulnerabilities(self, target_url: str, scan_type: str = "basic") -> Dict[str, Any]:
        """Scan for vulnerabilities using AI."""
        if not self._vuln_scanner:
            raise Exception("Vulnerability Scanner not initialized")
        
        try:
            # This would use the AI vulnerability scanner
            # For now, return a placeholder
            return {
                "target": target_url,
                "scan_type": scan_type,
                "vulnerabilities": [],
                "confidence": 0.0,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Vulnerability scan failed: {e}")
            raise
    
    async def generate_social_engineering_campaign(self, target_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate social engineering campaign using AI."""
        if not self._social_engineer:
            raise Exception("Social Engineer not initialized")
        
        try:
            # This would use the AI social engineer
            # For now, return a placeholder
            return {
                "target_info": target_info,
                "campaign": {
                    "messages": [],
                    "approach": "ethical_testing_only",
                    "confidence": 0.0
                },
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            self.logger.error(f"Social engineering generation failed: {e}")
            raise
    
    async def get_ai_capabilities(self) -> Dict[str, Any]:
        """Get comprehensive AI capabilities."""
        try:
            capabilities = {
                "provider": self._config["provider"],
                "model": self._config["model"],
                "modules": {
                    "chat_ai": self._chat_ai is not None and self._chat_ai.is_initialized,
                    "element_detector": self._element_detector is not None and self._element_detector.is_initialized,
                    "vuln_scanner": self._vuln_scanner is not None and self._vuln_scanner.is_initialized,
                    "social_engineer": self._social_engineer is not None and self._social_engineer.is_initialized,
                    "adaptive_evasion": self._adaptive_evasion is not None and self._adaptive_evasion.is_initialized,
                    "reconnaissance": self._reconnaissance is not None and self._reconnaissance.is_initialized
                },
                "features": [
                    "Natural language task generation",
                    "Website analysis and recommendations",
                    "Automation workflow suggestions",
                    "Security testing guidance",
                    "Form filling assistance",
                    "Data extraction planning",
                    "Error handling strategies",
                    "Element detection",
                    "Vulnerability scanning",
                    "Social engineering testing",
                    "Adaptive evasion techniques",
                    "Reconnaissance operations"
                ],
                "supported_actions": [
                    "navigate_to", "fill_form", "click_element", "extract_data",
                    "take_screenshot", "wait", "scroll", "create_jira_ticket",
                    "update_jira_status", "extract_jira_issues"
                ],
                "configuration": self._config
            }
            
            return capabilities
            
        except Exception as e:
            self.logger.error(f"Failed to get capabilities: {e}")
            raise
    
    async def cleanup(self) -> bool:
        """Cleanup AI service resources."""
        try:
            modules = [
                self._chat_ai,
                self._element_detector,
                self._vuln_scanner,
                self._social_engineer,
                self._adaptive_evasion,
                self._reconnaissance
            ]
            
            for module in modules:
                if module:
                    module.cleanup()
            
            self.logger.info("AI Service cleanup completed")
            return True
            
        except Exception as e:
            self.logger.error(f"AI Service cleanup failed: {e}")
            return False

# Global service instance
_ai_service: Optional[AIService] = None

async def get_ai_service() -> AIService:
    """Get or create AI service instance."""
    global _ai_service
    
    if _ai_service is None:
        _ai_service = AIService()
        if not await _ai_service.initialize():
            raise Exception("Failed to initialize AI Service")
    
    return _ai_service
